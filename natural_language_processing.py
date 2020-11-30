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


def findTweetsWithoutSentiment(uri, db, collection, query={'sentiment': {'$exists': False }}):
    return findTweets(uri, db, collection, query)






def sentimentAnalysis(cursor):
    ###
    # RETURN:    A list of dictionaries with fields of tweet info, including sentiment scores
    #            - fields: string text, datetime datetime, int likeCount, int retweetCount
    #                   int replyCount, int quoteCount, (list links - only when outlinks exist), 
    #                   dict sentiment('polarity', 'objectivity')
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