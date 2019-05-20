from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config


def main():
    training_data = load_data("data/nlu_data/")
    trainer = Trainer(config.load("nlu_config.yml"))
    interpreter = trainer.train(training_data)
    test_interpreter_dir = trainer.persist("./tests/models")
    parsing = interpreter.parse("hello")


if __name__ == "__main__":
    main()
