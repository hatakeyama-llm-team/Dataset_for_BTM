# トークナイザーの学習とtokenize

## setup
- Docker
~~~
sudo docker build -t llm .
sudo docker run --gpus all --shm-size='1gb' -it -p 8899:8888 -v .:/home/llm llm bash
~~~