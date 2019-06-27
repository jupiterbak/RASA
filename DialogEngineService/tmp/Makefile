.PHONY: clean train-nlu train-core cmdline server
.PHONY: clean test lint

TEST_PATH=./

help:
    @echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    train-nlu"
	@echo "        Train the natural language understanding using Rasa NLU."
	@echo "    train-core"
	@echo "        Train a dialogue model using Rasa core."
	@echo "    action-server"
	@echo "        Starts the server for custom action."
	@echo "    run-cmdline"
	@echo "        Starts the bot on the command line"
	@echo "    visualize"
	@echo "        Saves the story graphs into a file"

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build

run-actions:
	python -m rasa_core_sdk.endpoint --actions actions

train-nlu:
	python -m rasa_nlu.train -c nlu_config.yml --fixed_model_name nlu --data data/nlu_data/ -o models --project current --verbose

train-core:
	python -m rasa_core.train -d domain.yml -s data/core -c policies.yml --debug -o models/current/dialogue

action-server:
	python -m rasa_core_sdk.endpoint --actions actions

run-cmdline:
	make run-actions&
	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --debug --endpoints endpoints.yml

visualize:
	python -m rasa_core.visualize -s data/core/ -d domain.yml -o story_graph.png

train-online:
	python -m rasa_core.train -u models/current/nlu/ --online --core models/current/dialogue -d domain.yml -o story_graph.png

evaluate-core:
	python -m rasa_core.test --core models/current/dialogue -s data/core/ --fail_on_prediction_errors
