login
mock.onPost(/\/api\/login/).reply(config=>{
    //config like
    let request = {
        url: "/api/login",
        headers:{
            userKey: "userKey",
            password: "password",
            userType: "userType" // tel or studentID
        },
        body:{
            
        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            "type": "succeed",
            data:{
                image:"",
            }
        },
        //headers
        {
            token:"testtoken",
            tokendate: 300, 
            usertype: "admin", //admin ,customer
            username: "testcustomer"
        },
    ];
});
logout
mock.onPost(/\/api\/logout/).reply(config=>{
    //config like
    let request = {
        url: "/api/logout",
        headers:{
            token: "",
        },
        body:{

        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed" // need jump main page
        },
        //headers
        {},
    ];
});
searchBook
mock.onGet(/\/api\/book\/query\?(bookName|theme|authorName|ISBN)\=(.*)/).reply(config=>{
    //bookType in [tags]
    //config like
    let request = {
        url: "/api/book/query?<searchType=searchValue>",
        headers:{
            token: "" //?
        },
        body:{

        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed",
            data:{
                bookList:[{
                    name: "name1name1name1name1name1name1.¡£¡£",
                    ISBN: "isbn1",
                    auth: ["auth11", "auth12"],
                    position: {
                        room: "",
                        shelf: "",
                    },
                    language: [""],
                    theme: [""],
                    amount: 1,
                    image: "",
                }],
                filter:{
                    language: ["",""],
                    room: [""],
                    theme: ["", ""],
                }
            }
        },
        //headers
        {
            tokendate: 300 //?
        },
    ];
});
SearchBookInfo
mock.onGet(/\/api\/book\/info\?ISBN=(.*)/).reply(config=>{
    //config like
    let request = {
        url: "/api/book/info?ISBN=11111111",
        headers:{
            token: "" //£¿
        },
        body:{

        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed",
            data: {
                bookInfo: {
                    name: "bookinfo",
                    auth: ["bookinfo1"],
                    version: ["v1"],
                    ISBN: "bookinfo1",
                    publisher: "",
                    language: ["chiness",""],
                    position: {
                        room: "",
                        shelf: "",
                    },
                    theme: [""],
                    CLC: "",
                    amount: "3",
                    image: "",
                    description: "this is desc",
                    // if user is admin, copy's status is all
                    // if user is customer, copy's status only is Available
                    copys: [{
                            uuid: "111111",
                            status: "Available" //Available, Borrowed, Unavailable, Reserved
                        },{
                            uuid: "222222",
                            status: "Borrowed"
                        }
                    ],
                }
            }
        },
        //headers
        {
            tokendate: 300 //?
        },
    ];
});
searchUserInfo
mock.onGet(/\/api\/user\/info/).reply(config=>{
    //config like
    let request = {
        url: "/api/user/info",
        headers:{
            token: ""
        },
        body:{

        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed",
            data: {
                userInfo: {
                    userName: "",
                    uuid: "",
                    studentID: "",
                    tel: "",
                    balance: 300,
                    userImage: "",
                    orderNumber: "",
                    fine: 100,
                    /* ps: if user is admin, the orderNumber is all Applying order and Overdue order, the fine NaN
                           if user is customer, the orderNumber is now Overdue order, if the orderNumber > 0, the fine > 0, if the orderNumber = 0, the fine 0;
                    */
                }
            }
        },
        //headers
        {
            tokendate: 300
        },
    ];
});
Ð¡±àÍÆ¼ö
mock.onGet(/\/api\/book\/recommend/).reply(config=>{
    //bookType in [tags]
    //config like
    let request = {
        url: "/api/book/recommend",
        headers:{
            token: "" //?
        },
        body:{

        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed",
            data:{
                bookList:[{
                    name: "name1name1name1name1name1name1.¡£¡£",
                    ISBN: "isbn1",
                    description: "",
                    image: "",
                }]
            }
        },
        //headers
        {
            tokendate: 300 //?
        },
    ];
});
searchHistory
mock.onGet(/\/api\/user\/queryhistory/).reply(config=>{
    //config like
    let request = {
        url: "/api/user/queryhistory",
        headers:{
            token: "",
        },
        body:{

        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed",
            data: {
                bookList:[{
                    name: "apply1",
                    ISBN: "apply1",
                    position: {
                        room: "",
                        shelf: "",
                    },
                    theme: [""],
                    language: [""],
                    image: "",
                }]
            }
        },
        //headers
        {
            tokendate: 300
        },
    ];
});
searchOverDue

mock.onGet(/\/api\/user\/overduelist/).reply(config=>{
    //config like
    let request = {
        url: "/api/user/overduelist",
        headers:{
            token: "",
        },
        body:{

        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed",
            data: {
                orderList:[{
                    orderid: "",
                    applyDate: "",
                    
                    ISBN: "",
                    borrowDate: "",
                    overDays: 12, //now - borrowDate - 30
                    fine: 12,
                    bookName: "",
                    auth: [""],
                    image: "",
                    position: {
                        room: "",
                        shelf: "",
                    },
                    bookid: "",
                    amount: "",

                    userid: "",
                    userName: "",
                    balance: 250,
                }]
            }
        },
        //headers
        {
            tokendate: 300
        },
    ];
});
