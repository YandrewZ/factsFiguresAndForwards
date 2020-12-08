def findTweets(uri, db, collection, query):
    ###
    # RETURN:   A pymongo.cursor.Cursor object, containing a number of tweets to be analyzed
    #           - '.explain()' contains information about the cursor
    # 
    # uri: string, connection string
    # db: string, database name
    # collection: string, collection name
    # query: dict, filter used for the query operation
    ###

    import pymongo
    import bson
    from pymongo import InsertOne

    # connect to mongoDB
    client = pymongo.MongoClient(uri)
    collection_handle = client[db][collection]

    # retrieve entries and store in a cursor
    cursor = collection_handle.find(query)

    return cursor

### Some useful queries: 
# tweets without sentiment field - query={'sentiment': {'$exists': False }}
#

def findTweetsWithoutSentiment(uri, db, collection, query={'sentiment': {'$exists': False }}):
    return findTweets(uri, db, collection, query)






def sentimentAnalysis(cursor):
    ###
    # RETURN:    A list of dictionaries with fields of tweet info, including sentiment scores
    #            - fields: string text, datetime datetime, int likeCount, int retweetCount
    #                   int replyCount, int quoteCount, (list links - only when outlinks exist), 
    #                   dict sentiment{'polarity', 'objectivity'}
    # 
    # cursor: pymongo.cursor.Cursor, query result containing a number of tweets to be analyzed
    ###

    from textblob import TextBlob

    # initialize the list to be returned
    sentimentalTweets = []

    for i in cursor:
        sentimentalTweet = i
        blob = TextBlob(i['text'])
        sentiment = {'polarity': blob.sentiment.polarity, 'objectivity': blob.sentiment.subjectivity}
        sentimentalTweet['sentiment'] = sentiment
        sentimentalTweets.append(sentimentalTweet)
    

    return sentimentalTweets





def updateTweetsAfterSentimentAnalysis(sentimentalTweets, uri, db, collection):
    ###
    # RETURN:   A pymongo.results.BulkWriteResult object
    #           - 'bulk_api_result' field contains information about the operation
    #        AND
    #           A list of errored documents (tweet entries)
    # 
    # sentimenalTweets: list, of tweet entries to be updated in the database
    # uri: string, connection string
    # db: string, database name
    # collection: string, collection name
    ###

    import pymongo
    import bson
    from pymongo import UpdateOne

    # connect to mongoDB
    client = pymongo.MongoClient(uri)
    collection_handle = client[db][collection]

    
    # build bulk_write operations
    operations = []
    for i in sentimentalTweets:
        query = {'_id': i['_id'], 'text': i['text']}
        operation = {'$set': {'sentiment': i['sentiment']}}
        operations.append(UpdateOne(query, operation))

    errored_docs = []
    try:
        bulk_write_result = collection_handle.bulk_write(operations, ordered=False)
    except pymongo.errors.BulkWriteError as bre:
        errored_docs = [i['op'] for i in bre.details['writeErrors']]

    # Finish the operation and disconnect
    client.close()

    # return the operation result and a list of errored documents
    return bulk_write_result, errored_docs







def popularityStatistics(cursor, measure):
    ###
    # RETURN:   A dict of statistics of (the distribution of) one popularity measure in cursor
    #           - fields: int max, int min, int mean, int median,
    #                   (dict percentiles {
    #                                   '90th': {'count', 'sum_top_10%'},
    #                                   '80th': {'count', 'sum_top_20%'},
    #                                   ...
    #                                   '10th': {'count', 'sum_top_90%'},
    # 
    #                                   '75th': {'count', 'sum_top_25%'},
    #                                   '50th': {'count', 'sum_top_50%'},
    #                                   '25th': {'count', 'sum_top_75%'}
    #                    } - only when >10 tweets in cursor)
    # 
    # cursor: pymongo.cursor.Cursor object, of tweet entries to be analyzed
    # measure: string, one of 'likeCount', 'retweetCount', 'replyCount', 'quoteCount'
    ###
    
    import pymongo
    from statistics import mean, median, quantiles
    from math import floor

    countList = []
    for tweet in cursor:
        countList.append(tweet[measure])

    totalEntries = len(countList)

    # If number of entries less than or equal to 10, only calculate max, min, mean, and median
    if(len(countList) <= 10):
        rawStats = {
            'max': max(countList), 
            'min': min(countList), 
            'mean': mean(countList), 
            'median': median(countList)
        }
        return rawStats
    

    decileList = quantiles(countList, n=10)
    quartileList = quantiles(countList, n=4)

    percentiles = {
        # deciles
        '90th': {'count': decileList[8], 'sum_top_10%': sum(countList[:floor(totalEntries*0.1)])},
        '80th': {'count': decileList[7], 'sum_top_20%': sum(countList[:floor(totalEntries*0.2)])},
        '70th': {'count': decileList[6], 'sum_top_30%': sum(countList[:floor(totalEntries*0.3)])},
        '60th': {'count': decileList[5], 'sum_top_40%': sum(countList[:floor(totalEntries*0.4)])},
        '50th': {'count': decileList[4], 'sum_top_50%': sum(countList[:floor(totalEntries*0.5)])},
        '40th': {'count': decileList[3], 'sum_top_60%': sum(countList[:floor(totalEntries*0.6)])},
        '30th': {'count': decileList[2], 'sum_top_70%': sum(countList[:floor(totalEntries*0.7)])},
        '20th': {'count': decileList[1], 'sum_top_80%': sum(countList[:floor(totalEntries*0.8)])},
        '10th': {'count': decileList[0], 'sum_top_90%': sum(countList[:floor(totalEntries*0.9)])},
        # quartiles
        '75th': {'count': quartileList[2], 'sum_top_25%': sum(countList[:floor(totalEntries*0.25)])},
        '50th': {'count': quartileList[1], 'sum_top_50%': sum(countList[:floor(totalEntries*0.50)])},
        '25th': {'count': quartileList[0], 'sum_top_75%': sum(countList[:floor(totalEntries*0.75)])}
    }

    rawStats = {
        'max': max(countList), 
        'min': min(countList), 
        'mean': mean(countList), 
        'median': median(countList),
        'percentiles': percentiles,
    }
    return rawStats



def popularityStatistics(countList, measure):
    ### Overloaded Method
    # RETURN:   A dict of statistics of (the distribution of) one popularity measure in cursor
    #           - fields: int max, int min, int mean, int median,
    #                   (dict percentiles {
    #                                   '90th': {'count', 'sum_top_10%'},
    #                                   '80th': {'count', 'sum_top_20%'},
    #                                   ...
    #                                   '10th': {'count', 'sum_top_90%'},
    # 
    #                                   '75th': {'count', 'sum_top_25%'},
    #                                   '50th': {'count', 'sum_top_50%'},
    #                                   '25th': {'count', 'sum_top_75%'}
    #                    } - only when >10 tweets in cursor)
    # 
    # countList: list, of values of one popularity measure to be analyzed
    # measure: string, one of 'likeCount', 'retweetCount', 'replyCount', 'quoteCount'
    ###

    from statistics import mean, median, quantiles
    from math import floor

    totalEntries = len(countList)

    # If number of entries less than or equal to 10, only calculate max, min, mean, and median
    if(len(countList) <= 10):
        rawStats = {
            'max': max(countList), 
            'min': min(countList), 
            'mean': mean(countList), 
            'median': median(countList)
        }
        return rawStats
    

    decileList = quantiles(countList, n=10)
    quartileList = quantiles(countList, n=4)

    percentiles = {
        # deciles
        '90th': {'count': decileList[8], 'sum_top_10%': sum(countList[:floor(totalEntries*0.1)])},
        '80th': {'count': decileList[7], 'sum_top_20%': sum(countList[:floor(totalEntries*0.2)])},
        '70th': {'count': decileList[6], 'sum_top_30%': sum(countList[:floor(totalEntries*0.3)])},
        '60th': {'count': decileList[5], 'sum_top_40%': sum(countList[:floor(totalEntries*0.4)])},
        '50th': {'count': decileList[4], 'sum_top_50%': sum(countList[:floor(totalEntries*0.5)])},
        '40th': {'count': decileList[3], 'sum_top_60%': sum(countList[:floor(totalEntries*0.6)])},
        '30th': {'count': decileList[2], 'sum_top_70%': sum(countList[:floor(totalEntries*0.7)])},
        '20th': {'count': decileList[1], 'sum_top_80%': sum(countList[:floor(totalEntries*0.8)])},
        '10th': {'count': decileList[0], 'sum_top_90%': sum(countList[:floor(totalEntries*0.9)])},
        # quartiles
        '75th': {'count': quartileList[2], 'sum_top_25%': sum(countList[:floor(totalEntries*0.25)])},
        '50th': {'count': quartileList[1], 'sum_top_50%': sum(countList[:floor(totalEntries*0.50)])},
        '25th': {'count': quartileList[0], 'sum_top_75%': sum(countList[:floor(totalEntries*0.75)])}
    }

    # quartiles = {
    #     '75th': {'count': quartileList[2], 'sum_top_25%': sum(countList[:floor(totalEntries*0.25)])},
    #     '50th': {'count': quartileList[1], 'sum_top_50%': sum(countList[:floor(totalEntries*0.50)])},
    #     '25th': {'count': quartileList[0], 'sum_top_75%': sum(countList[:floor(totalEntries*0.75)])}
    # }
    rawStats = {
        'max': max(countList), 
        'min': min(countList), 
        'mean': mean(countList), 
        'median': median(countList),
        'percentiles': percentiles,
    }
    return rawStats






def generallStatistics(cursor, datetime):
    ###
    # RETURN:   A dict of statistics of all four popularity measures in cursor
    #           - fields: datetime datetime, int totalEntries,
    #                   dict likeStats (rawStats from popularityStatistics),
    #                   dict retweetStats (rawStats from popularityStatistics),
    #                   dict replyStats (rawStats from popularityStatistics), 
    #                   dict quoteStats (rawStats from popularityStatistics), 
    # 
    # cursor: pymongo.cursor.Cursor object, of tweet entries to be analyzed
    # datetime: string, date attribute of the tweets being analyzed - '2020-06-25'
    ###

    import pymongo
    
    totalEntries = cursor.count()
    
    # Likes
    likeCursor = cursor.clone()
    likeCursor.sort('likeCount', pymongo.DESCENDING)
    likeStats = popularityStatistics(likeCursor, 'likeCount')

    # retweets
    retweetCursor = cursor.clone()
    retweetCursor.sort('retweetCount', pymongo.DESCENDING)
    retweetStats = popularityStatistics(retweetCursor,'retweetCount')

    # replies
    replyCursor = cursor.clone()
    replyCursor.sort('replyCount', pymongo.DESCENDING)
    replyStats = popularityStatistics(replyCursor,'replyCount')
 
    # quotes
    cursor.sort('quoteCount', pymongo.DESCENDING)
    quoteStats = popularityStatistics(cursor,'quoteCount')

    stats = {
        'datetime': datetime,
        'totalEntries': totalEntries,
        'likeStats': likeStats,
        'retweetStats': retweetStats,
        'replyStats': replyStats,
        'quoteStats': quoteStats
    }

    return stats


def generallStatistics(tweetsList, datetime):
    ### Overloaded Method
    # RETURN:   A dict of statistics of all four popularity measures in cursor
    #           - fields: datetime datetime, int totalEntries,
    #                   dict likeStats (rawStats from popularityStatistics),
    #                   dict retweetStats (rawStats from popularityStatistics),
    #                   dict replyStats (rawStats from popularityStatistics), 
    #                   dict quoteStats (rawStats from popularityStatistics), 
    # 
    # tweetsList: list, of tweet entries to be analyzed
    # datetime: string, date attribute of the tweets being analyzed - '2020-06-25'
    ###

    totalEntries = len(tweetsList)
    
    # Likes
    likesList = [i['likeCount'] for i in tweetsList]
    likesList.sort(reverse=True)
    likeStats = popularityStatistics(likesList, 'likeCount')

    # retweets
    retweetsList = [i['retweetCount'] for i in tweetsList]
    retweetsList.sort(reverse=True)
    retweetStats = popularityStatistics(retweetsList,'retweetCount')

    # replies
    repliesList = [i['replyCount'] for i in tweetsList]
    repliesList.sort(reverse=True)
    replyStats = popularityStatistics(repliesList,'replyCount')
 
    # quotes
    quotesList = [i['quoteCount'] for i in tweetsList]
    quotesList.sort(reverse=True)
    quoteStats = popularityStatistics(quotesList,'quoteCount')

    stats = {
        'datetime': datetime,
        'totalEntries': totalEntries,
        'likeStats': likeStats,
        'retweetStats': retweetStats,
        'replyStats': replyStats,
        'quoteStats': quoteStats
    }

    return stats
