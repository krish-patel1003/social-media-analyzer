from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class PostBase(BaseModel):
    post_type: str
    likes: int
    shares: int
    comments: int
    tags: List[str]
    caption: str
    impressions: int
    sentiment: float
    posted_date: str
    engagement_timeline: Dict[str, int]

class TemporalAnalysis(BaseModel):
    day: str
    avg_likes: float
    avg_shares: float
    avg_comments: float

class TagAnalysis(BaseModel):
    tag: str
    avg_likes: float
    avg_shares: float
    avg_comments: float

class SentimentAnalysis(BaseModel):
    positive: float
    neutral: float
    negative: float
