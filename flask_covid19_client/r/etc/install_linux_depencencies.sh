#!/usr/bin/env bash

function add_apt_repo_for_r(){
	# update indices
	sudo apt update -qq
	# install two helper packages we need
	sudo apt install --no-install-recommends software-properties-common dirmngr
	# add the signing key (by Michael Rutter) for these repos
	# To verify key, run gpg --show-keys /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
	# Fingerprint: 298A3A825C0D65DFD57CBB651716619E084DAB9
	wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
	# add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
	sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
}

function apt_update(){
	sudo apt update -qq && sudo apt upgrade
}

function add_apt_repo_for_cran(){
	sudo add-apt-repository ppa:c2d4u.team/c2d4u4.0+
}

function install_R(){
	sudo apt install --no-install-recommends r-base
}

function add_apt_repo_cran_poppler(){
	sudo add-apt-repository -y ppa:cran/poppler
}

function install_unbuntu_dev(){
	sudo apt-get install -y \
		littler \
		libpoppler-cpp-dev \
		libxml2-dev \
		libssl-dev \
		libssh2-1-dev \
		libpq-dev \
		libpq5 \
		libpoppler-cpp-dev \
		libssl-dev \
		libssh2-1-dev \
		libudunits2-dev
}

function main(){
	#add_apt_repo_for_r
	apt_update
	install_R
	#add_apt_repo_cran_poppler
	install_unbuntu_dev
}

main

