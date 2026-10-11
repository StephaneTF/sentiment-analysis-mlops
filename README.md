## Model versioning and rollback

Model version 1.0 uses a TF-IDF vectorizer and logistic regression model
saved in the `models/` folder. Its validation accuracy was 0.7966 and
its F1-score was 0.7990.

The model was trained with Sentiment140's two sentiment classes:
0 = negative and 4 = positive. The API returns either "negative" or
"positive"; it does not return a neutral class.

GitHub Actions publishes Docker images with a commit-specific tag:
`sha-<commit-SHA>`. This tag identifies the exact project version,
including its model files.

To roll back, replace `<commit-SHA>` with the SHA of an earlier
successful commit, then run:

    docker pull bobyfos/sentiment-api:sha-<commit-SHA>
    docker run --rm -p 5001:5000 bobyfos/sentiment-api:sha-<commit-SHA>