# SYNTH-ITA: SYNthetic THeft dataset for ITAlian event extraction

SYNTH-ITA is a dataset of  **10,000** synthetic news articles about theft events, generated using the **Llama-3-8B-Instruct** model. The dataset is designed for **Event Extraction** related to crime events from news articles and is based on the annotation schema for crime news articles introduced with the Italian dataset [DICE](https://github.com/federicarollo/Italian-Crime-News).

## Repository Structure

The GitHub repository contains the following directories:

- `annotation_generation`: This folder contains a library for pseudo-randomly generating fictitious annotations by selecting plausible values for entities involved in theft events.
- `news_generation`: Includes the Python script used to generate synthetic theft news articles based on the fictitious annotations created in the previous step.
- `prompts`: Contains three versions of the prompts used during the experiments:
  - **V1.0**
  - **V1.1**
  - **V2.0**
- `synthetic_dataset`: Contains the final synthetic dataset. For each article, the following are provided:
  - The generated fictitious annotation.
  - The news article created using **prompt V1.1**.
  - The news article created using **prompt V2.0**.
- `manual_evaluation`: Includes subsets of the dataset used for the manual evaluation of the generated news articles, comparing results from **prompt V1.1** and **prompt V2.0**.

## Usage

This dataset is suitable for **NLP research**, particularly in **Event Extraction**, **Question Answering**, and **crime event analysis**.

## License

Please refer to the repository for licensing details and usage restrictions.
