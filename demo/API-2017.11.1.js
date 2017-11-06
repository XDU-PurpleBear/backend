import normalAxios from "axios";
import MockAdapter from "axios-mock-adapter";

let axios = normalAxios.create();

let theme = ["Arts","Business", "Computer Science", "Data Science", "Engineering", "Language Skills", "Life Science", "Mathematics", "Personal Development", "Physics", "Social Science"];

let orderStatus = ["Applying", "Borrowing ", "Finished", "Overdue", "Invalid"];

let bookCopyStatus = ["Available", "Unavailable", "Borrowed", "Reserved"];

let mock = new MockAdapter(axios);

//All failed response body is {type: "failed", errorReason: "errorReason"} headers is {"tokendate": 300}


// 2017/10/31
mock.onPost(/\/api\/login/).reply(config=>{
    不变
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

mock.onPost(/\/api\/logout/).reply(config=>{
    不变
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

mock.onGet(/\/api\/book\/query\?(bookName|bookType|authorName|ISBN)\=(.*)/).reply(config=>{   **** +ISBN*****
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
                    name: "name1name1name1name1name1name1.。。",
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

// need add history
mock.onGet(/\/api\/book\/info\?ISBN=(.*)/).reply(config=>{
    不变
    //config like
    let request = {
        url: "/api/book/info?ISBN=11111111",
        headers:{
            token: "" //？
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

mock.onGet(/\/res\/image\/name/).reply(config=>{
  GetImage(info)
  info: {
    "url":
  }
  return:{
    "status":
    "img":{
      "data":
      "type":
    }

  }

    //config like
    let request = {
        url: "/res/image/<johnshitImage>",
        headers:{},
        body:{

        }
    }
    //response
    return [
        //status
        200,
        //body
        "asdasda1278agd8sd", //二进制数据
        //headers
        {
            "Content-Type": ""
        },
    ];
});


// 2017/11/1
// TODO: check
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


// only admin
mock.onGet(/\/api\/user\/searchinfo/).reply(config=>{
  SearchUserInfo(info)
  info:{
    token: "",
    studentID: "",
  }
  return:{
    "status":
    "data":{

    }
  }
    //config like
    let request = {
        url: "/api/user/info",
        headers:{
            token: "",
            studentID: "",
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
                }
            }
        },
        //headers
        {
            tokendate: 300
        },
    ];
});


// only admin
mock.onPost(/\/api\/signup/).reply(config=>{
  Signup(info)
  info:{
    username: "userName", //not only
    studentid: "",//only
    balance: "",
    deposit: 300, // only value
    password: "password",
    tel: "tel",//only
    token: "",
  }
  return:{
    "status":
    "tokendate":
  }
    //config like
    let request = {
        url: "/api/signup",
        headers:{
            userName: "userName", //not only
            studentID: "",//only
            balance: "",
            deposit: 300, // only value
            password: "password",
            tel: "tel",//only
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

        },
        //headers
        {
            tokendate: 300,
        },
    ];
});

// only admin
mock.onPost(/\/api\/user\/editinfo/).reply(config=>{ ***改密码时，要查询密码是否为空，如果为空或者None， 此时不调用改密码，否则调用改密码。

    UserChangePassword(info)
    info: {
      "token": ,
      "password":
    }
    UserChangeBalance(info)
    info: {
      "token": ,
      "balance": (是充的金额，还是充完之后的金额)
    }
    //config like
    let request = {
        url: "/api/user/editinfo",
        headers:{
            balance: "",
            password: "password",
            uuid: "",
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

        },
        //headers
        {
            tokendate: 300,
        },
    ];
});

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
                    name: "name1name1name1name1name1name1.。。",
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

// only admin
mock.onPost(/\/api\/book\/add/).reply(config=>{
    //config like
    let request = {
        url: "/api/book/add",
        headers:{
            token: ""
        },
        body:{
            name: "",
            auth: ["", ""],
            ISBN: "",
            publisher: "",
            CLC: "",
            version: "",
            description: "",
            language: [""],
            theme: [""],
            amount: "",
            image: {
                data: "", //二进制格式。默认格式jpg
                type: ""
            }

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
                    position: ["101", "2"],
                    theme: [""],
                    CLC: "",
                    amount: "3",
                    image: "",
                    description: "this is desc",
                    copys: [{
                            uuid: "111111",
                            status: "available" //available, borrowed, unavailable, reserved
                        },{
                            uuid: "222222",
                            status: "borrowed"
                        }
                    ],
                }
            }
        },
        //headers
        {
            tokendate: 300
        },
    ];
});

// only admin
mock.onPost(/\/api\/book\/addcopy/).reply(config=>{
    //config like
    let request = {
        url: "/api/book/addcopy",
        headers:{
            token: ""
        },
        body:{
            ISBN: "",
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
                uuid: "aaaaaaa",
            }
        },
        //headers
        {
            tokendate: ""
        },
    ];
});

// only admin
// borrowed can't be deleted
mock.onPost(/\/api\/book\/deletecopy/).reply(config=>{
    //config like
    let request = {
        url: "/api/book/deletecopy",
        headers:{
            token: ""
        },
        body:{
            uuid: "" //book's copy uuid
        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed"
        },
        //headers
        {
            tokendate: ""
        },
    ];
});

// only admin
// check bookcopy status
mock.onPost(/\/api\/book\/editcopy/).reply(config=>{
    //config like
    let request = {
        url: "/api/book/deletecopy",
        headers:{
            token: ""
        },
        body:{
            uuid: "", //book's copy uuid
            status: ""
        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed"
        },
        //headers
        {
            tokendate: ""
        },
    ];
});

// only customer
mock.onPost(/\/api\/user\/editimage/).reply(config=>{
    //config like
    let request = {
        url: "/api/user/editimage",
        headers:{
            token: ""
        },
        body:{
            image: "",
            type: ""
        }
    }
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed"
        },
        //headers
        {
            tokendate: ""
        },
    ];
});


// TODO: check for db
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


























mock.onGet(/\/api\/user\/applylist/).reply(config=>{
    //config like
    let request = {
        url: "/api/user/applylist",
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
                    auth: ["a1"],
                    position: "b111",
                    amount: 1,
                    image: "",
                    timeLimits: "1",
                    uuid: "uuid1",
                },{
                    name: "apply2",
                    ISBN: "apply2",
                    auth: ["a2"],
                    position: "b222",
                    amount: 2,
                    image: "",
                    timeLimits: "2",
                    uuid: "uuid2",
                },{
                    name: "apply2",
                    ISBN: "apply2",
                    auth: ["a2"],
                    position: "b222",
                    amount: 2,
                    image: "",
                    timeLimits: "2",
                    uuid: "uuid2",
                },{
                    name: "apply2",
                    ISBN: "apply2",
                    auth: ["a2"],
                    position: "b222",
                    amount: 2,
                    image: "",
                    timeLimits: "2",
                    uuid: "uuid2",
                },{
                    name: "apply2",
                    ISBN: "apply2",
                    auth: ["a2"],
                    position: "b222",
                    amount: 2,
                    image: "",
                    timeLimits: "2",
                    uuid: "uuid2",
                },{
                    name: "apply2",
                    ISBN: "apply2",
                    auth: ["a2"],
                    position: "b222",
                    amount: 2,
                    image: "",
                    timeLimits: "2",
                    uuid: "uuid2",
                }]
            }
        },
        //headers
        {
            tokendate: 300
        },
    ];
});

mock.onGet(/\/api\/user\/returnlist/).reply(config=>{
    //config like
    let request = {
        url: "/api/user/returnlist",
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
                    auth: ["a1"],
                    position: "b111",
                    amount: 1,
                    image: "",
                    timeLimits: "1"
                },{
                    name: "apply2",
                    ISBN: "apply2",
                    auth: ["a2"],
                    position: "b222",
                    amount: 2,
                    image: "",
                    timeLimits: "2"
                }]
            }
        },
        //headers
        {
            tokendate: 300
        },
    ];
});

mock.onGet(/\/api\/user\/borrowlist/).reply(config=>{
    //config like
    let request = {
        url: "/api/user/borrowlist",
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
                    auth: ["a1"],
                    position: "b111",
                    amount: 1,
                    image: "",
                    timeLimits: "1"
                },{
                    name: "apply2",
                    ISBN: "apply2",
                    auth: ["a2"],
                    position: "b222",
                    amount: 2,
                    image: "",
                    timeLimits: "2"
                }]
            }
        },
        //headers
        {
            tokendate: 300
        },
    ];
});

mock.onPost(/\/api\/user\/apply/).reply(config=>{
    //config like
    let request = {
        url: "/api/user/apply",
        headers:{
            token: ""
        },
        body:{
            uuids: [""],

        }
    }
    console.log(config);
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed",
        },
        //headers
        {
            tokendate: ""
        },
    ];
});

mock.onPost(/\/api\/user\/borrow/).reply(config=>{
    //config like
    let request = {
        url: "/api/user/borrow",
        headers:{
            token: ""
        },
        body:{
            uuids: [""],

        }
    }
    console.log(config);
    //response
    return [
        //status
        200,
        //body
        {
            type: "succeed",
        },
        //headers
        {
            tokendate: ""
        },
    ];
});


export {
    axios
};
