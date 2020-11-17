def unshortenLinks(outlinks, unshortener):
    ### 
    # RETURN: A list of unshortened links
    #
    # outlinks: list, of links from the tweet object - tweet.outlinks
    # unshortener: unshortener object, from the unshortenit library - UnshortenIt(default_timeout=30)
    ###
    
    links = []
    for link in outlinks:
        # unshorten all the links
        try:
            link = unshortener.unshorten(link, force=True, unshorten_nested=True)
        except:
            continue
        links.append(link)
    return links



def generateMessage(minimum_likes, data_list):
    ###
    # RETURN: A string message that contains number of minimum likes, number of tweets, 
    #            dates of latest and earlier tweets
    # 
    # minimum_likes: int, the mnimum number of likes used in the final query
    # data_list: list, of tweet entries retrieved in the final query
    ###
    
    result_stats = 'With a minimum of {} likes, we found {} tweets for you.'.format(minimum_likes, len(data_list))

    result_datetimes = ' The latest of them was posted at {} and the earliest was posted at {}.'.format(data_list[0]['datetime'], data_list[len(data_list)-1]['datetime'])

    return result_stats + result_datetimes



def retrieveTweets(keyword, startDate, endDate, maxTweets, minimum_likes=0):
    ###
    # RETURN: 
    #         A list of dictionaries with fields of tweet info 
    #         - fields: string text , datetime datetime , int likeCount, int retweetCount
    #                   int replyCount, int quoteCount, (list links - only when outlinks exist)
    #     OR
    #         An Exception
    # 
    # keyword: string, the hashtag keyword, without # - 'blacklivesmatter'
    # startDate: string, the first day of the query, including year - '2020-05-25'
    # endDate: string, last day of the query, including year - '2020-06-25'
    # maxTweets: int, maximum number of tweets to be retrieved - 1000
    # minimum_likes: int, default is 0, query filter for searching tweets with a minimum number of likes - 100000
    ###

    import snscrape.modules.twitter as sntwitter

    # initialze the unshortener
    from unshortenit import UnshortenIt
    unshortener = UnshortenIt(default_timeout=30)

    # Initiliaze the list of tweets to be returned
    tweets = []
    
    ## Limit the maxTweets retrieved here using min_lkes_filter
    min_likes_filter = ''
    if(minimum_likes > 0):
        min_likes_filter = "min_faves:{}".format(minimum_likes)

    ## Build scraper  
    result = sntwitter.TwitterHashtagScraper(
        keyword + 
        ' {} since:{} until:{} lang:en -filter:replies'.format(min_likes_filter, startDate, endDate)).get_items() 
        # example queryString - 'blacklivesmatter min_faves:1 since:2020-06-01 until:2020-06-02
        #                        lang:en  -filter:replies'
        # queryString syntax: filter:links - search only tweets with links
        # queryString syntax: min_faves:1 - search tweets with a minimum of 1 like
        
        
    try:
        for i, tweet in enumerate(result):
            if(i % 50 == 0):
                print("This is the {}th tweet with a minimum of {} likes".format(i, minimum_likes))

            if(i >= maxTweets) :
                print('END - maxTweets of {}'.format(i))
                break

            # Tweets without outlinks won't have the 'links' field
            tweet_data = {
                        'text': tweet.renderedContent, 
                        'datetime': tweet.date, 
                        'likeCount': tweet.likeCount, 
                        'retweetCount': tweet.retweetCount, 
                        'replyCount': tweet.replyCount, 
                        'quoteCount': tweet.quoteCount }
        
            # Only create the 'links' field for tweets that have outlinks
            if(tweet.outlinks != []):
                links = unshortenLinks(tweet.outlinks, unshortener)
                tweet_data['links'] = links
        
            tweets.append(tweet_data)

    except Exception as e:
        print('Exception:')
        print(e)
        return e

    
    return tweets




def fetchTopTweetsIterative(keyword, startDate, endDate, maxTweets):
    ###
    # RETURN:    A list of dictionaries with fields of tweet info, length not guaranteed to be maxTweets
    #            - fields: string text , datetime datetime , int likeCount, int retweetCount
    #                   int replyCount, int quoteCount, (list links - only when outlinks exist)
    #         AND
    #            A string message that contains number of minimum likes, number of tweets, 
    #            dates of latest and earlier tweets
    #     OR:   
    #            An Exception
    #         AND
    #            A string of Error Message - 'An error has occured'
    # 
    # keyword: string, the hashtag keyword, without # - 'blacklivesmatter'
    # startDate: string, the first day of the query, including year - '2020-05-25'
    # endDate: string, last day of the query, including year - '2020-06-25'
    # maxTweets: int, maximum number of tweets to be retrieved - 1000
    ###

    # Initialize minimum_likes
    minimum_likes = 10000000

    # Iniitialize current_data_list and desired_data_list (to be returned)
    current_data_list = retrieveTweets(keyword, startDate, endDate, maxTweets, minimum_likes)
    # Error-Handling
    if(not isinstance(current_data_list, list)):
        # In this case, current_data_list will be the exception
        return current_data_list, 'An error has occured'
    desired_data_list = current_data_list.copy()
    
    ## Lower the minimum likes iteratively
    while(len(current_data_list) < maxTweets):
        if(minimum_likes == 0):
            break
        minimum_likes = (minimum_likes * 3) // 4
        desired_data_list = current_data_list.copy()
        current_data_list = retrieveTweets(keyword, startDate, endDate, maxTweets, minimum_likes)
        # Error-Handling
        if(not isinstance(current_data_list, list)):
            # In this case, current_data_list will be the exception
            return current_data_list, 'An error has occured'

    # Gather some information about the retrieved tweets
    message = generateMessage(minimum_likes, desired_data_list)

    return desired_data_list, message
    




def writeToMongoDB(data_list, uri, db, collection):
    ###
    # RETURN:   A pymongo.results.BulkWriteResult object
    #           - 'bulk_api_result' field contains information about the operation
    #        AND
    #           A list of errored documents (tweet entries)
    # 
    # data_list: list, of tweet entries to be written to the database
    # uri: string, connection string
    # db: string, database name
    # collection: string, collection name
    ###

    import pymongo
    import bson
    from pymongo import InsertOne

    # connect to mongoDB
    client = pymongo.MongoClient(uri)
    collection_handle = client[db][collection]

    # build bulk_write operations
    operations = []
    for i in data_list:
        operations.append(InsertOne(i))
    
    errored_docs = []
    try:
        bulk_write_result = collection_handle.bulk_write(operations, ordered=False)
    except pymongo.errors.BulkWriteError as bre:
        errored_docs = [i['op'] for i in bre.details['writeErrors']]

    # Finish the operation and disconnect
    client.close()

    # return the operation result and a list of errored documents (tweet entries)
    return bulk_write_result, errored_docs
