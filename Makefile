.PHONY: help run_local migrate_local upgrade_local db before_commit

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

before_commit: ## before commit trigger
	echo 'nothing to do'

before_run_prod: ## before production run trigger
	pybabel compile -d 'app/translations' -D 'messages admin'

pybabel_extract: ## pybabel extract
	pybabel extract \
		--project=mitlahateb \
		--version=1.0.0 \
		-o messages.po \
		-F babel.cfg \
		-k lazy_gettext \
		--input-dir=app

pybabel_update_he: ## pybabel update
	pybabel update \
		-i messages.po \
		-d app/translations \
		--previous \
		-l he

run_prod: before_run_prod ## production run and it's dependencies
	FLASK_APP=app.server flask run -h $(HOST) -p $(PORT)

run_local: ## run heroku local instance
	heroku local

migrate_local: ## migrate heroku db local instance
	heroku local:run flask db migrate

upgrade_local: # upgrade heroku db local instance
	heroku local:run flask db upgrade

upgrade_remote: # upgrade heroku db local instance
	heroku run FLASK_APP=app.server flask db upgrade

db_kill: ## kill local postgres instance with docker
	docker stop postgres
	docker rm postgres
