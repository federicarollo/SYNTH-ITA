# SYNTH-ITA: SYNthetic THeft dataset for ITAlian event extraction

SYNTH-ITA is a dataset of  **10,000** synthetic news articles about theft events, generated using three Large Language Models: **Llama-3-8B-Instruct**, **Qwen2.5-7B-Instruct**, **Qwen2.5-14B-Instruct**. The dataset is designed for **Event Extraction** related to crime events from news articles and is based on the annotation schema for crime news articles introduced with the Italian dataset [DICE](https://github.com/federicarollo/Italian-Crime-News).

## Repository Structure

The GitHub repository contains the following directories:

- `annotation_generation`: This folder contains a library for pseudo-randomly generating fictitious annotations by selecting plausible values for entities involved in theft events.
- `news_generation`: Includes the Python script used to generate synthetic theft news articles based on the fictitious annotations created in the previous step.
- `prompts`: Contains three versions of the prompts used during the experiments:
  - **V1.0**
  - **V1.1**
  - **V2.0**
- `synthetic_dataset`: Contains the final synthetic dataset. For each article, the following are provided:
  - The generated fictitious annotations.
  - The news articles created with **Llama-3-8B-Instruct**.
  - The news articles created with **Qwen2.5-7B-Instruct**.
  - The news articles created with **Qwen2.5-14B-Instruct**.
  - The news articles created with **DeepSeek-V2-Chat**.

## Usage

This dataset is suitable for **NLP research**, particularly in **Event Extraction**, **Question Answering**, and **crime event analysis**.

## License

Please refer to the repository for licensing details and usage restrictions.
