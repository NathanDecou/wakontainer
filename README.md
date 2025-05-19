<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a id="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/NathanDecou/wakontainer">
    <img src="images/logo.jpeg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Wakontainer</h3>

  <p align="center">
    Automatically start (and stop) your docker containers when needed.
    <br />
    <a href="https://github.com/NathanDecou/wakontainer/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/NathanDecou/wakontainer/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#deploy-with-gunicorn">Deploy with gunicorn</a></li>
    <li><a href="#deploy-with-docker-compose">Deploy with Docker compose</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#demo">Demo</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Wakontainer sits between a reverse proxy and a web service running in a container. When a request is made to access the web service, the request is first forward to wakontainer which starts the container if needed. Wakontainer also stops containers when no requests were made during a certain time.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Python][Python.org]][Python-url]
- [![Flask][Flask.com]][Flask-url]
- [![Python Docker SDK][DockerSDK.io]][DockerSDK-url]
- [![Gunicorn][Gunicorn.org]][Gunicorn-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

1. Have Python installed
2. Have Docker installed
3. Have a reverse proxy installed (e.g nginx)

### Installation

1. Clone this repo `git clone https://github.com/NathanDecou/wakontainer`
2. Go inside the folder `cd wakontainer`
3. Install the required packages `python3 -m pip install -r requirements.txt`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Deploy with Gunicorn

1. Create the service file (see [example](conf_examples/wakontainer.service))
2. Reload systemctl daemon `systemctl daemon-reload`
2. Configure your reverse proxy to use wakontainer as an auth service (see [example](conf_examples/mysite-nginx.conf))
3. Configure your container to enable wakontainer (see [example](conf_examples/mycontainer-compose.yaml))
4. Create (or start) your container `docker compose create`
5. Start wakontainer `systemctl start wakontainer`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Deploy with Docker compose

1. Create the image `docker build . -t wakontainer`
2. Create a compose file (see [example](conf_examples/wakontainer-compose.yaml))
3. Run the container `docker compose up`

## Demo
Here is a video that demonstrates the basic of wakontainer. The lags are due to the way I screenrecorded the video.

[demo.webm](https://github.com/user-attachments/assets/d6f6c7bb-66a7-4b45-8175-b3910b78d84e)

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GNU General Public License v3.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments


- [Choose an Open Source License](https://choosealicense.com)
- [Best README Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Python.org]: https://img.shields.io/badge/Python-ffde57?style=for-the-badge&logo=python&logoColor=4584b6
[Python-url]: https://www.python.org/
[Flask.com]: https://img.shields.io/badge/Flask-47AFC2?style=for-the-badge&logo=flask&logoColor=black
[Flask-url]: https://flask.palletsprojects.com/en/stable/
[DockerSDK.io]: https://img.shields.io/badge/Python%20Docker%20SDK-0963D1?style=for-the-badge&logo=docker&logoColor=white
[DockerSDK-url]: https://docker-py.readthedocs.io/en/stable/
[Gunicorn.org]: https://img.shields.io/badge/Gunicorn-white?logo=gunicorn&style=for-the-badge&logoColor=489746
[Gunicorn-url]: https://gunicorn.org/
