import pandas as pd

# List of customer reviews
reviews = [
    "Great product, very useful!",
    "Poor quality and bad customer service.😡",
    "Average performance, nothing special.",
    "Exceeded my expectations, fantastic!",
    "Terrible, not worth the money.😞",
    "Quite good, but could be improved.",
    "Mediocre at best, not recommended.",
    "Wonderful design, highly recommended!",
    "Awful experience, would not buy again.",
    "Solid product, good value for the price.",
    "Highly satisfied with the purchase.",
    "The product broke after a few uses.",
    "I would definitely buy this again!😄",
    "Not as described, very disappointed.",
    "Customer service was really helpful.",
    "It works perfectly as expected.",
    "I had a terrible experience with this.",
    "Well worth the money.",
    "Waste of time and money.",
    "Absolutely love this product!",
    "It didn’t work as advertised.",
    "Very reliable and easy to use.",
    "I had higher expectations, sadly disappointed.",
    "Delivered quickly, works as intended.",
    "Horrible quality, won’t buy again.",
    "This is the best purchase I’ve made.",
    "It stopped working after a month.",
    "I’m quite pleased with this product.",
    "Very cheap material, not durable.",
    "Fantastic performance for the price.",
    "Extremely frustrating experience.",
    "User-friendly and well-designed.",
    "Not worth the price at all.🙁",
    "Better than expected!",
    "The instructions were very unclear.",
    "Would definitely recommend to others.",
    "Very underwhelming experience.",
    "Does the job, no complaints.",
    "I regret purchasing this item.",
    "Great value for money!😃",
    "Arrived damaged, very disappointed.",
    "Exceeded my expectations!",
    "Not what I was hoping for.",
    "Happy with the purchase overall.",
    "Total waste of money.",
    "Amazing product, highly satisfied!",
    "Not durable, broke after a few uses.",
    "Fantastic design and great quality.",
    "Wouldn’t recommend to others.",
    "Excellent value, would buy again.",
    "Terrible product, avoid at all costs."
]

# Create a DataFrame with the reviews
df = pd.DataFrame(reviews, columns=["review_text"])

# Save the DataFrame to an Excel file
df.to_excel("customer_reviews.xlsx", index=False)
