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



# def generateMessage(minimum_likes, data_list):
#     ###
#     # RETURN: A string messa    ge that contains number of minimum likes, number of tweets, 
#     #            dates of latest and earlier tweets
#     # 
#     # minimum_likes: int, the mnimum number of likes used in the final query
#     # data_list: list, of tweet entries retrieved in the final query
#     ###
    
#     result_stats = 'With a minimum of {} likes, we found {} tweets for you.'.format(minimum_likes, len(data_list))

#     result_datetimes = ' The latest of them was posted at {} and the earliest was posted at {}.'.format(data_list[0]['datetime'], data_list[len(data_list)-1]['datetime'])

#     return result_stats + result_datetimes



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
            if(i >= maxTweets) :
                break

            # Tweets without outlinks won't have the 'links' field

            tweet_data = {
                        'text': tweet.content, 
                        'datetime': tweet.date, 
                        'likeCount': tweet.likeCount, 
                        'retweetCount': tweet.retweetCount, 
                        'replyCount': tweet.replyCount, 
                        'quoteCount': tweet.quoteCount
                        }
        
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




def fetchTopTweetsIterative(keyword, startDate, endDate, maxTweets, minimum_likes=1000000, declineRate = 0.2):
    ###
    # RETURN:    A list of dictionaries with fields of tweet info, length not guaranteed to be maxTweets
    #            - fields: string text , datetime datetime , int likeCount, int retweetCount
    #                   int replyCount, int quoteCount, (list links - only when outlinks exist)
    #         AND
    #               
    #            A string 'TEMP'. No purpose, but necessary for NODE and PYTHON interaction 
    #            
    #            OLD ------------------------------------------------------------------------
    #            A string message that contains number of minimum likes, number of tweets, 
    #            dates of latest and earlier tweets
    #            ----------------------------------------------------------------------------
    #     OR:   
    #            An Exception
    #         AND
    #            A string of Error Message - 'An error has occured'
    # 
    # keyword: string, the hashtag keyword, without # - 'blacklivesmatter'
    # startDate: string, the first day of the query, including year - '2020-05-25'
    # endDate: string, last day of the query, including year - '2020-06-25'
    # maxTweets: int, maximum number of tweets to be retrieved - 1000
    # minimum_likes: int, default is 1000, searching tweets starting from a minimum number of likes - 5000
    # declineRate: float, default is 0.2, the rate at which minimum_likes decreases. Range is (0,1), if out of 
    #              range, converts it to fit the range
    ###

    # 0 < declineRate < 1 
    from math import floor
    if(declineRate == 0 or declineRate == 1):
        print("declineRate cannot be {}. Using default value 0.2".format(declineRate))
        declineRate = 0.75
    elif(abs(declineRate) > 1):
        declineRate = round(1/abs(declineRate), 2)
        print("0 < declineRate < 1. Using declineRate = 1 / |declineRate| = {}".format(declineRate))
    elif(declineRate < 0):
        declineRate = abs(declineRate)
        print("0 < declineRate < 1. Using declineRate = |declineRate| = {}".format(declineRate))


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
        minimum_likes = floor(minimum_likes * declineRate)
        desired_data_list = current_data_list.copy()
        current_data_list = retrieveTweets(keyword, startDate, endDate, maxTweets, minimum_likes)
        # Error-Handling
        if(not isinstance(current_data_list, list)):
            # In this case, current_data_list will be the exception
            return current_data_list, 'An error has occured'

    # Gather some information about the retrieved tweets
    # message = generateMessage(minimum_likes, desired_data_list)

    return desired_data_list, 'TEMP' # , message
    




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

### 
# nodejs communication module
#
# utilizes the sys and json libraries to communicate with the server
# functions through the use of child processes within the main server framework
import sys
import json

# function for turning dictionaries, tuples, and more, into json serializble blocks
def toJson(data):
    return json.dumps(data, default=str)


# unicode reconfiguration to allow for ptinting/writing to/from console
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# ni: node input
#
# ni can take two forms
# this depends on what function the python script is serving at the time
#
# the two modes are
#
# retreival :
#   mode used to perform the retreival of tweets
#   ni object (dictionary) will take the following form:
#   {
#     mode       : String 'retreive',          // mode detailing whether python file should
#                                              // scrape for tweets or write to database
#     hashtag    : String '#hashtag',          // hashtag to scrape
#     startdate  : String 'yyyy-mm-dd',        // start date for scrape
#     enddate    : String 'yyyy-mm-dd',        // end date for scrape
#     maxtweets  : Int 500,                    // maximum number of tweets to be retreived (default 500, max of TBD)
#     minlikes   : Int 0,                      // unused value for minimum number of likes
#                                              // for scraped tweet. kept for future use
#     authkey    : String 'auth-key',          // utilized in nodejs server framework security
#     error      : Boolean false,              // utilized in nodejs server framework
#   }
#
#
# write :
#   mode used to write documents into the database
#   ni object (dictionary) will take the following form:
#   {
#     mode       : String 'write',             // mode detailing whether python file should
#                                              // scrape for tweets or write to database
#     data_list  : TBD
#     uri        : String 'uri',               // uri string for access to the database
#     db         : String 'db_name',           // database name
#     collection : String 'collection_name',   // collection name
#
#     authkey    : String 'auth-key',          // utilized in nodejs server framework security
#     error      : Boolean false,              // utilized in nodejs server framework
#   }
#   foStr:  String ""   || Identifier used to mark the print statement as the final output
#   capStr: String ""   || Identifier used to mark beggining of data to be parsed
#   sid:    Int    0    || Scraper ID, Identifier used in NodeJS functions to process, transfer,
#                       || and manage the correct set of data for each scraper. (Multi-scraper func.)
#
# *dictionaries may include extra fields not highlited here, but are likely trivial*

# parse JSON string into python dictionary
ni     = json.loads(sys.argv[1])
foStr  = sys.argv[2]
capStr = sys.argv[3]
sid    = sys.argv[4]

# collect tweets
if ni["mode"] == "retreive":
    output = fetchTopTweetsIterative(ni["hashtag"], ni["startdate"], ni["enddate"], ni["maxtweets"])
    output_str = toJson(output[0])
    o_format = "json"

# write to database
elif ni["mode"] == "write":
    output = writeToMongoDB(ni["data_list"], ni["uri"], ni["db"], ni["collection"])
    output_str = repr(output[1])
    o_format = "r/w mongodb"

# output printed to communicate with nodejs
# 
# output is returned in a specif manner that allows nodejs
# to understand this is the output containing the final data
#
# the output will be a string formatted as follows:
# """
# $$FINAL_OUTPUT$$
# $$DATA$$
# {
#   "$format$" : Str "json" || "r/w mongodb",    //string displaying whether the
#                                                //format of the data will be a json
#                                                //or something else (TBD)
#   "$data$" : List [] || TBD                    //data returned from python script
#   "$SID$"  : Int 12345                         //Identifier for the scraper. Used
#                                                //to avoid data bleed in mongodb
# }
# """
final_output = f"""{foStr}{capStr}{{"$format$" : "{o_format}","$data$" : {output_str},"$SID$" : {sid}}}"""
print(final_output)
###
