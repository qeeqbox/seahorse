echo -e "\nQeeqBox Seahorse v$(jq -r '.version' info) starter script -> https://github.com/qeeqbox/seahorse"
echo -e "Current servers (HTTP, HTTPS, SSH, FTP, RDP, VNC, SMB, MONGO, MYSQL and LDAP)\n"\

setup_requirements () {
	sudo apt update -y
	sudo apt install -y linux-headers-$(uname -r) docker.io jq xdg-utils curl
	sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	which docker-compose && echo "Good"
	which docker && echo "Good"
}

wait_on_web_interface () {
echo ''
until $(curl --silent --head --fail http://localhost:5601/login --output /dev/null); do
echo -ne "\n[\033[47m\033[0;31mInitializing project in progress..\033[0m]\n"
sleep 5
done
echo ''
xdg-open http://localhost:5601/login
}

test_project () {
	sudo docker-compose -f docker-compose-test.yml up --build
}

dev_project () {
	sudo docker-compose up --build
}

stop_containers () {
	sudo docker-compose down -v
	sudo docker stop $(sudo docker ps -aq)
} 

deploy_aws_project () {
	echo "Will be added later on"
}

auto_configure_test () {
	setup_requirements
	test_project
}

auto_configure () {
	setup_requirements
	dev_project
}

if [[ "$1" == "auto_test" ]]; then
	stop_containers
	wait_on_web_interface & 
	auto_configure_test
	stop_containers 
fi

if [[ "$1" == "auto_configure" ]]; then
	stop_containers
	wait_on_web_interface & 
	auto_configure
	stop_containers 
fi

while read -p "`echo -e '\nChoose an option:\n1) Setup requirements (docker, docker-compose)\n2) Run auto configuration test\n3) Run auto configuration\n>> '`"; do
  case $REPLY in
    "1") setup_requirements;;
    "2") auto_configure;;
    "3") auto_configure_test;;
    *) echo "Invalid option";;
  esac
done

