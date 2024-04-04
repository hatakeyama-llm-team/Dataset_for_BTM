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
#include <algorithm>

#define MAX_LINE_LENGTH 102400
#define MAX_HASH_SIZE 1000000
#define SIMILARITY_THRESHOLD 0.3

typedef struct {
    std::vector<std::string> texts;
    std::string representative;
} TextGroup;

size_t hash(const char *s, uint32_t seed) {
    uint64_t output[2];
    MurmurHash3_x64_128(s, strlen(s), seed, &output);
    return output[0];
}

double hash_similarity(const char *s1, const char *s2) {
    size_t hash1 = hash(s1, 0);
    size_t hash2 = hash(s2, 0);
    size_t max_hash = std::max(hash1, hash2);
    size_t min_hash = std::min(hash1, hash2);
    return (double)min_hash / max_hash;
}

void write_output_file(const std::string &file_name, const std::vector<TextGroup> &groups, const std::string &output_dir) {
    char output_file[1024];
    snprintf(output_file, sizeof(output_file), "%s/%s", output_dir.c_str(), file_name.c_str());

    FILE *fp_out = fopen(output_file, "w");
    if (fp_out == NULL) {
        printf("Error creating output file %s\n", output_file);
        return;
    }

    for (const auto &group : groups) {
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
                        double similarity = hash_similarity(text, group.representative.c_str());
                        if (similarity >= SIMILARITY_THRESHOLD) {
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

            // 処理が完了したファイルを出力
            write_output_file(entry->d_name, file_text_groups[entry->d_name], output_dir);
        }
    }

    closedir(dir);

    return 0;
}