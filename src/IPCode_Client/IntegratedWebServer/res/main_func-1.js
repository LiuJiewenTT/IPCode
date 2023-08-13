/*
    File name: main_func-1.js
    Author: LiuJiewenTT(on Github.com)
    Description: 
        This script is to receive or send IPv6 address.
    Rights Declaration:
        The codes have something sourced from the Internet. External sourced codes may be edited and only belong to the license mentioned in the corresponding part. If not explicitly indicated, codes will be under the license of this project.
*/

// ________________ 
// Part 1

class WebSocketTool {
    // websocket初始化
    constructor(name, url) {
        this.name = name;
        this.url = url;
    }
    initWebSocket() {
        // 这里是new一个socket实例。后面填写socket服务器地址，应该都有端口号的。还可以传其他的参数，具体的可以搜一下socket初始化的一些参数。
        // this.websocket = new WebSocket(this.$Url.ChatWebSocket);
        this.websocket = new WebSocket(this.url);
        // 连接错误
        this.websocket.onerror = this.setErrorMessage;
        // 连接成功
        this.websocket.onopen = this.setOnopenMessage;
        // 收到消息的回调
        this.websocket.onmessage = this.screenMsg;
        // 连接关闭的回调
        this.websocket.onclose = this.setOncloseMessage;
        // 监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
        window.onbeforeunload = this.onbeforeunload;
    }
    // 监听窗口关闭事件
    onbeforeunload() {
        this.websocket.close();
    }
    // socket连接失败回调
    setErrorMessage(res) {
        console.log('连接失败', res);
        this.socketclose = true;
    }
    // socket连接成功回调
    setOnopenMessage(res) {
        this.socketclose = false;
        console.log('websocket连接已打开');
        // socket链接成功后在发送登录socket的验证方式。当然你们的socket不需要登录的话，下面登录可以删掉。
        let data = {
            type: 'login',
            user_id: this.uid,
            room_id: this.room_id
        };
        this.websocket.send(JSON.stringify(data));
    }
    // scoket关闭回调
    setOncloseMessage(res) {
        console.log('连接已关闭');
        // this.socketclose = true;
    }
    //接收socket信息
    screenMsg(res) {
        // socket返回的数据是JSON格式的需要转换一下。
        var datas = JSON.parse(res.data)
    }
}

// ———————————————— Codes being further developed in this part are based on:
// 版权声明：本文为CSDN博主「简_洋」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
// 原文链接：https://blog.csdn.net/Even_ycp/article/details/128492940
// ________________ This part of codes are under: CC 4.0 BY-SA
// ________________ End of Part 1