# Dataset

This project uses the CREMA-D (Crowd-sourced Emotional Multimodal Actors Dataset)
for speech emotion recognition.

## CREMA-D

The raw CREMA-D audio files are not included in this repository.

The speech emotion recognition component uses the `AudioWAV` portion of CREMA-D,
containing 7,442 audio samples from 91 actors.

The model recognises six emotion classes:

- Angry
- Disgust
- Fear
- Happy
- Neutral
- Sad

## Metadata

`crema_metadata.csv` contains the metadata used by the project, including:

- filename
- actor ID
- sentence code
- emotion label
- intensity
- train/validation/test split

The dataset is split by actor rather than randomly by audio sample. This ensures
that speakers appearing in the training set do not appear in the validation or
test sets, reducing the risk of speaker leakage.

The split contains:

- Training: 73 actors, 5,967 samples
- Validation: 9 actors, 737 samples
- Test: 9 actors, 738 samples

## Dataset Location

After obtaining CREMA-D, the `AudioWAV` directory should be available locally.

The dataset location can be configured using the `CREMA_ROOT` environment
variable. If it is not set, the training and evaluation scripts use their
default relative dataset location.

The raw dataset should not be committed to the repository.