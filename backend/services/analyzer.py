from datetime import datetime, timedelta

class EngagementAnalyzer:
    @staticmethod
    async def analyze_temporal_patterns(collection):
        """Analyze engagement patterns by day of the week."""
        cursor = collection.find({})
        docs = [doc async for doc in cursor]

        day_metrics = {}
        for doc in docs:
            day_of_week = datetime.fromisoformat(doc["posted_date"]).strftime('%A')
            if day_of_week not in day_metrics:
                day_metrics[day_of_week] = {
                    "likes": 0, "shares": 0, "comments": 0, "count": 0
                }
            day_metrics[day_of_week]["likes"] += doc["likes"]
            day_metrics[day_of_week]["shares"] += doc["shares"]
            day_metrics[day_of_week]["comments"] += doc["comments"]
            day_metrics[day_of_week]["count"] += 1

        return {
            day: {
                "avg_likes": round(metrics["likes"] / metrics["count"], 2),
                "avg_shares": round(metrics["shares"] / metrics["count"], 2),
                "avg_comments": round(metrics["comments"] / metrics["count"], 2)
            }
            for day, metrics in day_metrics.items()
        }

    @staticmethod
    async def analyze_tag_co_occurrence(collection):
        """Analyze tag co-occurrence and their engagement impact."""
        cursor = collection.find({})
        docs = [doc async for doc in cursor]

        tag_metrics = {}
        for doc in docs:
            for tag in doc["tags"]:
                if tag not in tag_metrics:
                    tag_metrics[tag] = {"likes": 0, "shares": 0, "comments": 0, "count": 0}
                tag_metrics[tag]["likes"] += doc["likes"]
                tag_metrics[tag]["shares"] += doc["shares"]
                tag_metrics[tag]["comments"] += doc["comments"]
                tag_metrics[tag]["count"] += 1

        return {
            tag: {
                "avg_likes": round(metrics["likes"] / metrics["count"], 2),
                "avg_shares": round(metrics["shares"] / metrics["count"], 2),
                "avg_comments": round(metrics["comments"] / metrics["count"], 2)
            }
            for tag, metrics in tag_metrics.items()
        }


    @staticmethod
    async def analyze_sentiment_impact(collection):
        """Analyze sentiment impact on engagement."""
        cursor = collection.find({})
        docs = [doc async for doc in cursor]

        positive, neutral, negative = {"likes": 0, "count": 0}, {"likes": 0, "count": 0}, {"likes": 0, "count": 0}

        for doc in docs:
            if doc["sentiment"] > 0.1:
                bucket = positive
            elif doc["sentiment"] < -0.1:
                bucket = negative
            else:
                bucket = neutral

            bucket["likes"] += doc["likes"]
            bucket["count"] += 1

        return {
            "positive": round(positive["likes"] / positive["count"], 2) if positive["count"] else 0,
            "neutral": round(neutral["likes"] / neutral["count"], 2) if neutral["count"] else 0,
            "negative": round(negative["likes"] / negative["count"], 2) if negative["count"] else 0
        }

    @staticmethod
    async def analyze_post_lifespan(collection):
        """Analyze the lifespan of posts in terms of engagement."""
        cursor = collection.find({})
        docs = [doc async for doc in cursor]

        lifespan_metrics = {}
        for doc in docs:
            timeline = doc["engagement_timeline"]
            total_engagement = sum(timeline.values())
            lifespan_metrics[doc["_id"]] = {"total_engagement": total_engagement}

        return lifespan_metrics