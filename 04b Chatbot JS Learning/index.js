// var data = {
//     chatinit:{
//         title:["Hello <span class='emoji'> &#128075; </span>",
//         "You can select one of the below options to begin with!"],
//         options:['Ask about the product', 'Ask about customer reviews', 'Ask for customized recommendations']
//     }
// }

var data= {
    chatinit:{
        title: ["Hello <span class='emoji'> &#128075; </span>","You can select one of the below options to begin with!"],
        options: ["Product Enquiry","Customer review", "Personalized Product Recommendations"]
    },

    product:{
        title: ['Please ask your questions about the product!'],
        options:[]
    },

    customer:{
        title:['Would you like to know the overall ratings or the overall review summary?'],
        options:['Review Ratings', "Review Summary"]
    },

    personalized:{
        title:['Please select all the features you would like to consider for the similar product search'],
        options:['Color', 'Material']
    }
}

document.getElementById("init").addEventListener("click",showChatBot);
var cbot= document.getElementById("chat-box");

var len1= data.chatinit.title.length;

function showChatBot(){
    console.log(this.innerText);
    if(this.innerText=='START CHAT'){
        document.getElementById('test').style.display='block';
        document.getElementById('init').innerText='CLOSE CHAT';
        initChat();
    }
    else{
        location.reload();
    }
}

function initChat(){
    j=0;
    cbot.innerHTML='';
    for(var i=0;i<len1;i++){
        setTimeout(handleChat,(i*500));
    }
    setTimeout(function(){
        showOptions(data.chatinit.options)
    },((len1+1)*500))
}

var j=0;
function handleChat(){
    console.log(j);
    var elm= document.createElement("p");
    elm.innerHTML= data.chatinit.title[j];
    elm.setAttribute("class","msg");
    cbot.appendChild(elm);
    j++;
    handleScroll();
}

function showOptions(options){
    for(var i=0;i<options.length;i++){
        var opt= document.createElement("span");
        var inp= '<div>'+options[i]+'</div>';
        opt.innerHTML=inp;
        opt.setAttribute("class","opt");
        opt.addEventListener("click", handleOpt);
        cbot.appendChild(opt);
        handleScroll();
    }
}

function handleOpt(){
    console.log(this);
    var str= this.innerText;
    var textArr= str.split(" ");
    var findText= textArr[0];

    document.querySelectorAll(".opt").forEach(el=>{
        el.remove();
    })
    var elm= document.createElement("p");
    elm.setAttribute("class","test");
    var sp= '<span class="rep">'+this.innerText+'</span>';
    elm.innerHTML= sp;
    cbot.appendChild(elm);

    console.log(findText.toLowerCase());
    var tempObj= data[findText.toLowerCase()];
    if (findText.toLowerCase() === 'product') {
        // If Product Enquiry option is selected, show input text box
        showInputBox();
    } else {
        handleResults(tempObj.title, tempObj.options);
    }
}

// Function to show input text box for Product Enquiry
function showInputBox() {
    var inputBox = document.createElement("input");
    inputBox.setAttribute("type", "text");
    inputBox.setAttribute("id", "productEnquiryInput");
    inputBox.setAttribute("placeholder", "Enter your question here...");
    cbot.appendChild(inputBox);

    var sendBtn = document.createElement("button");
    sendBtn.innerText = "Send";
    sendBtn.setAttribute("class", "sendBtn");
    sendBtn.addEventListener("click", handleUserInput);
    cbot.appendChild(sendBtn);

    handleScroll(); // Scroll to bottom after showing input box
}

// Function to handle user's input message
function handleUserInput() {
    var userInput = document.getElementById("userInput").value;
    var userMsgContainer = document.createElement("div");
    userMsgContainer.setAttribute("class", "user-msg");
    userMsgContainer.innerHTML = '<span class="msg">' + userInput + '</span>';
    cbot.appendChild(userMsgContainer);
    handleScroll(); // Scroll to bottom after sending user message

    // Clear input box after sending message
    document.getElementById("userInput").value = "";

    // Simulate bot's response after a delay (for demonstration)
    setTimeout(function () {
        handleDelay("Bot's response to user message: " + userInput);
    }, 1000);
}


function handleDelay(title){
    var elm= document.createElement("p");
        elm.innerHTML= title;
        elm.setAttribute("class","msg");
        cbot.appendChild(elm);
}


function handleResults(title,options){
    for(let i=0;i<title.length;i++){
        setTimeout(function(){
            handleDelay(title[i]);
        },i*500)
    }

    // After showing all results, show input box if the title contains the specific message
    setTimeout(function () {
        if (title.includes('Please ask your questions about the product!')) {
            showInputBox();
        }
    }, title.length * 500);
}

function handleOptions(options){
    for(var i=0;i<options.length;i++){
        var opt= document.createElement("span");
        opt.innerHTML=inp;
        opt.setAttribute("class","opt");
        cbot.appendChild(opt);
    }
    var opt= document.createElement("span");

    opt.innerHTML=inp;
    opt.setAttribute("class","opt link");
    cbot.appendChild(opt);
    handleScroll();
}

function handleScroll(){
    var elem= document.getElementById('chat-box');
    elem.scrollTop= elem.scrollHeight;
}