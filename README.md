

<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Python Discord Bot</h3>
</p>



<!-- ABOUT THE PROJECT -->
## About The Project


Hey this is my Python Bot its not the cleanest code but it works the most time. I worked on it 1 Month becouse of the problems with the Docker API but this is my Work I hope it could help you. 


<!-- GETTING STARTED -->

This are things you need to install
* python 3
  ```
  https://www.python.org/
  ```
* Docker
  ```
  https://www.docker.com/get-started
  ```

### Installation

1. You have to edit all tokes[Discord, Github, pastbin]
2. Clone the repo
   ```sh
   git clone https://github.com/lordLegal/pythondiscordbot.git
   ```
3. Install Python packages
   ```sh
   python3 -m pip install -r requirements.txt
   ```
4. add the docker fiels
   ```sh
   cd py3dockerfile
   docker -t mypython:3-alpine .
   cd ..
   cd py2docker
   docker -t mypython:2-alpine .
   ```
5. Run the Bot
  ```sh
  python3 bot.py
  ```



