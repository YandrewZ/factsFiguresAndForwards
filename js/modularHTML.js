let timeline = document.getElementById('timeline');

let datesLeft = true;
let turn_right = true;
let universal_date_index = 0;
let current_article_index = 0;

let top_bp = document.getElementById("timeline_top_bp");
let mid_right_bp = document.getElementById("timeline_mid_right_bp");
let mid_left_bp = document.getElementById("timeline_mid_left_bp");

$(window).scroll(function() {
   if($(window).scrollTop() + $(window).height() > $(document).height() - 400) {
       extendFile();
   }
});

function extendFile() {
    if(datesLeft){
        // let tempArt = fetch_HEAD(global_links_array[universal_date_index], 0);
        try{
            let finished_top = createTop();

            const cached_date = addDays(m25, universal_date_index);
            const cached_date_index = universal_date_index;

            finished_top.getElementsByClassName("top-node-date")[0].innerText = Months[cached_date.getMonth()] + " " + getDayAsStr(cached_date.getDate());
            if(articlesByDate[universal_date_index].length > 4){
                timeline.appendChild(finished_top);
                for(let i = 0; i < 2; i++){
                    if(turn_right){
                        tempCard = createRightMid();
                    } else{
                        tempCard = createLeftMid();
                    }
                    turn_right = !turn_right;

                    tempCard.getElementsByClassName("article-title")[0].innerText = articlesByDate[universal_date_index][i].link;
                    tempCard.getElementsByClassName("article-title")[0].href = articlesByDate[universal_date_index][i].link;
                    tempCard.getElementsByClassName("source-url")[0].innerText = `Appearances on #BlackLivesMatter: ${articlesByDate[universal_date_index][i].mentions}\nLikes on source Tweet: ${articlesByDate[universal_date_index][i].likes}`;
                    tempCard.getElementsByClassName("introductory-snippet")[0].innerText = '';
                    timeline.appendChild(tempCard);
                }
                if(turn_right){
                    tempCard = createRightMid();
                } else{
                    tempCard = createLeftMid();
                }

                turn_right = !turn_right;
                tempCard.getElementsByClassName("article-title")[0].innerText = `View ${articlesByDate[universal_date_index].length - 2} more links shared on ${Months[cached_date.getMonth()]} ${getDayAsStr(cached_date.getDate())}`;
                tempCard.getElementsByClassName("article-title")[0].setAttribute('onclick', `javascript:displayList(${cached_date_index}, '${cached_date}')`);
                tempCard.getElementsByClassName("article-title")[0].href = 'extra_html/link_list.html';
                tempCard.getElementsByClassName("introductory-snippet")[0].innerText = `${articlesByDate[universal_date_index][2].link}\n${articlesByDate[universal_date_index][3].link}\n...`;
                tempCard.getElementsByClassName("source-url")[0].innerText = '';
                timeline.appendChild(tempCard);

            } else{
                timeline.appendChild(finished_top);
                for(let i = 0; i < articlesByDate[universal_date_index].length; i++){
                    if(turn_right){
                        tempCard = createRightMid();
                    } else{
                        tempCard = createLeftMid();
                    }
                    turn_right = !turn_right;

                    tempCard.getElementsByClassName("article-title")[0].innerText = articlesByDate[universal_date_index][i].link;
                    tempCard.getElementsByClassName("article-title")[0].href = articlesByDate[universal_date_index][i].link;
                    tempCard.getElementsByClassName("source-url")[0].innerText = `Appearances on #BlackLivesMatter: ${articlesByDate[universal_date_index][i].mentions}\nLikes on source Tweet: ${articlesByDate[universal_date_index][i].likes}`;
                    tempCard.getElementsByClassName("introductory-snippet")[0].innerText = '';
                    timeline.appendChild(tempCard);
                }
            }
            universal_date_index++;
            if(universal_date_index >= articlesByDate.length){
                datesLeft = false;
            }
        } catch (e) {
            console.log(e);
        }
    }
}

//fucntion for creating a card on the right side of the screen
function createRightMid(){
    let mid_right_clone = mid_right_bp.cloneNode(true);
    mid_right_clone.id = "";
    mid_right_clone.style = "";
    return mid_right_clone;
}

//function for creating a card on the left side of the screen
function createLeftMid(){
    let mid_left_clone = mid_left_bp.cloneNode(true);
    mid_left_clone.id = "";
    mid_left_clone.style = "";
    return mid_left_clone;
}

//function for creating a pointer for the date
function createTop() {
    let top_clone = top_bp.cloneNode(true);
    top_clone.id = global_dates_array[universal_date_index];
    top_clone.style = "";
    return top_clone;
}

// async function fetch_HEAD(url, index){
//     console.log(url);
//     let data = '';
//     const proxies = ["https://cors-anywhere.herokuapp.com/", "https://cors-proxy.htmldriven.com/?url=", "https://thingproxy.freeboard.io/fetch/"]
//     if(index < proxies.length){
//         try {
//             const response = await fetch(proxies[index] + url, {method: 'GET'});
//             data = await response.text();
//         } catch(e) {
//             console.log(e);
//             fetch_HEAD(url, index + 1);
//         }
//     } else {
//         console.log('All proxies have failed');
//     }
//     let parser = new DOMParser();
//     let xmlDoc = parser.parseFromString(data, 'text/xml');
//     console.log(xmlDoc);
//     let ret = {};
//     try{ret.image = xmlDoc.querySelector('[rel="image_src"]')[0].href; return ret;} catch{}
//     try{ret.image = xmlDoc.querySelector('[property="og:image"]')[0].content; return ret;} catch{}
//
//     return ret;
// }
