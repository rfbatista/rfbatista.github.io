server:
	 hugo server -wDs . -d dev
deploy:
	sh ./scripts/deploy.sh
install:
	sh ./scripts/install.sh
	

check:
	sh ./scripts/check.sh

browser-check:
	sh ./scripts/browser-check.sh
