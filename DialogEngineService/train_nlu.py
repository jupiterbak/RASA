from rasa.nlu.training_data import load_data
from rasa.nlu.model import Trainer
from rasa.nlu import config


def main():
    # loading the nlu training samples
    training_data = load_data("data/nlu/")

    # trainer to educate our pipeline
    trainer = Trainer(config.load("config.yml"))

    # train the model!
    interpreter = trainer.train(training_data, verbose=True)

    # store it for future use
    model_directory = trainer.persist("models", fixed_model_name="nlu")


if __name__ == "__main__":
    main()
