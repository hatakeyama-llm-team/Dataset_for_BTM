#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <unordered_map>
#include "smhasher/src/MurmurHash3.h"
#include "rapidjson/include/rapidjson/document.h"
#include "rapidjson/include/rapidjson/stringbuffer.h"
#include "rapidjson/include/rapidjson/writer.h"
#include <vector>

#define MAX_LINE_LENGTH 102400
#define MAX_HASH_SIZE 1000000
#define SIMILARITY_THRESHOLD 0.4
#define MAX_COMPARE_LENGTH 1024

typedef struct {
    std::vector<std::string> texts;
    std::string representative;
} TextGroup;

size_t hash(const char *s, uint32_t seed) {
    uint64_t output[2];
    MurmurHash3_x64_128(s, strlen(s), seed, &output);
    return output[0];
}

int levenshtein_distance(const char *s1, const char *s2, int max_length) {
    int len1 = std::min(strlen(s1), (size_t)max_length);
    int len2 = std::min(strlen(s2), (size_t)max_length);
    int matrix[len1 + 1][len2 + 1];

    for (int i = 0; i <= len1; i++) {
        matrix[i][0] = i;
    }
    for (int j = 0; j <= len2; j++) {
        matrix[0][j] = j;
    }

    for (int j = 1; j <= len2; j++) {
        for (int i = 1; i <= len1; i++) {
            if (s1[i - 1] == s2[j - 1]) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                int deletion = matrix[i - 1][j] + 1;
                int insertion = matrix[i][j - 1] + 1;
                int substitution = matrix[i - 1][j - 1] + 1;
                matrix[i][j] = std::min(deletion, std::min(insertion, substitution));
            }
        }
    }

    return matrix[len1][len2];
}

double similarity(const char *s1, const char *s2) {
    int distance = levenshtein_distance(s1, s2, MAX_COMPARE_LENGTH);
    int max_length = std::min(std::max(strlen(s1), strlen(s2)), (size_t)MAX_COMPARE_LENGTH);
    return 1.0 - (double)distance / max_length;
}


int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <input_dir> <output_dir>\n", argv[0]);
        return 1;
    }

    char *input_dir = argv[1];
    char *output_dir = argv[2];

    DIR *dir = opendir(input_dir);
    if (dir == NULL) {
        printf("Error opening input directory\n");
        return 1;
    }

    std::unordered_map<std::string, std::vector<TextGroup>> file_text_groups;

    // ファイルの総数を取得
    int total_files = 0;
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) {
            total_files++;
        }
    }
    rewinddir(dir);

    // 処理したファイル数を初期化
    int processed_files = 0;

    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) {
            processed_files++;
            printf("Processing file %d/%d: %s\n", processed_files, total_files, entry->d_name);

            char input_file[1024];
            snprintf(input_file, sizeof(input_file), "%s/%s", input_dir, entry->d_name);

            FILE *fp = fopen(input_file, "r");
            if (fp == NULL) {
                printf("Error opening file %s\n", input_file);
                continue;
            }

            char line[MAX_LINE_LENGTH];
            while (fgets(line, sizeof(line), fp)) {
                rapidjson::Document doc;
                doc.Parse(line);

                if (!doc.HasParseError() && doc.HasMember("text")) {
                    const char *text = doc["text"].GetString();

                    bool found_group = false;
                    for (auto &group : file_text_groups[entry->d_name]) {
                        double sim = similarity(text, group.representative.c_str());
                        if (sim >= SIMILARITY_THRESHOLD) {
                            group.texts.push_back(text);
                            if (group.representative.length() < strlen(text)) {
                                group.representative = text;
                            }
                            found_group = true;
                            break;
                        }
                    }

                    if (!found_group) {
                        TextGroup new_group;
                        new_group.texts.push_back(text);
                        new_group.representative = text;
                        file_text_groups[entry->d_name].push_back(new_group);
                    }
                }
            }

            fclose(fp);
        }
    }

    closedir(dir);


    for (const auto &file_groups : file_text_groups) {
        char output_file[1024];
        snprintf(output_file, sizeof(output_file), "%s/%s", output_dir, file_groups.first.c_str());

        FILE *fp_out = fopen(output_file, "w");
        if (fp_out == NULL) {
            printf("Error creating output file %s\n", output_file);
            continue;
        }

        for (const auto &group : file_groups.second) {
            rapidjson::StringBuffer buffer;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);

            writer.StartObject();
            writer.Key("text");
            writer.String(group.representative.c_str());
            writer.EndObject();

            fprintf(fp_out, "%s\n", buffer.GetString());
        }

        fclose(fp_out);
    }

    return 0;
}