let csvFile = 'blacklivesmatter_05-25_06-12_topTweets_urlSummary.csv';

let global_article_list = undefined;

let global_links_array = [];
let global_likes_array = [];
let global_mntns_array = [];
let global_dates_array = [];

let global_line_length = undefined;

//fetch csv files and parse them into text.
async function getData(url){
    const response = await fetch(url);
    const data = await response.text();
    global_article_list = data;
    global_line_length = listElementCounter(global_article_list);
    console.log(global_line_length);
    initArrays();
    createArticleObjects();
}

function listElementCounter(list){
    let tempList  = list;
    let tempList2 = list;
    let newLineIndex = tempList.indexOf('\n');
    while(newLineIndex < list.length - 1 && newLineIndex != -1){
        tempList2 = tempList;
        tempList = tempList.slice(tempList.indexOf('\n') + 1);
        newLineIndex = tempList.indexOf('\n')
    }

    return tempList2.slice(0, tempList2.indexOf(','))
}

function initArrays(){
    let tempList = global_article_list.slice(global_article_list.indexOf('\n') + 1);
    for(var i = 0; i <= global_line_length; i++){
        tempList = tempList.slice(tempList.indexOf(',') + 1);

        global_links_array.push(tempList.slice(0, tempList.indexOf(',')));
        tempList = tempList.slice(tempList.indexOf(',') + 1);

        global_dates_array.push(tempList.slice(0, tempList.indexOf(',')));
        tempList = tempList.slice(tempList.indexOf(',') + 1);

        global_likes_array.push(tempList.slice(0, tempList.indexOf(',')));
        tempList = tempList.slice(tempList.indexOf(',') + 1);

        global_mntns_array.push(tempList.slice(0, tempList.indexOf('\n')));
        tempList = tempList.slice(tempList.indexOf('\n') + 1);

    }
}

function createArticleObjects(){
    for(var i = 0; i < global_links_array.length; i++){
        articles.push(new Article(global_links_array[i],
        global_dates_array[i],
        global_likes_array[i],
        global_mntns_array[i]));
    }
}

getData(csvFile);
