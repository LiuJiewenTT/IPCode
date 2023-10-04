/*
    File name: main_func-2.js
    Author: LiuJiewenTT(on Github.com)
    Description:
        This script is about unsorted functions.
    Rights Declaration:
        The codes have something taken from the Internet. External sourced codes may be edited and only belong to the license mentioned in the corresponding part. If not explicitly indicated, codes will be under the license of this project.
*/

// ________________
// Part 1
function js_2_onload(){
    // let func_name='onload'
    // checkNewestStatus()
    checkNewestStatus_ver2()
}

function wrap_an_element(element, wrapper_label){
    let wrapper = document.createElement(wrapper_label)
    wrapper.appendChild(element.cloneNode(deep=true))
    element.parentNode.replaceChild(wrapper, element)
}

function wrap_del_an_element(element){
    wrap_an_element(element, "del")
}

// ________________ End of Part 1
// ________________
// Part 2

function checkNewestStatus(){
    let span_ipv6_address = document.getElementById("span_ipv6_address")
    let currentIPv6Address = document.getElementById("code_ipv6_address").innerText
    let currentIPv6Prefix = document.getElementById("code_ipv6_prefix").innerText
    console.log("[checkNewestStatus]:Begin")
    if( currentIPv6Address != null ){
        let code_ipv6_address = document.getElementById("code_ipv6_address")
        let status_icon_ipv6_address = document.getElementById("status_icon_ipv6_address")
        let if_newest = false
        // Show status
        if( code_ipv6_address.innerText === "None" ){
            console.log("[Warning]: code_ipv6_address is None")
            wrap_del_an_element(code_ipv6_address)
            status_icon_ipv6_address.style.background = "red"
        }
        else {
            status_icon_ipv6_address.style.background = "green"
            let storedIPv6Address = localStorage.getItem("IPv6_Address")
            if( storedIPv6Address !== currentIPv6Address ){
                console.log("[Info]: New IPv6_Address")
                if_newest = true
                // storedIPv6Address = currentIPv6Address
                localStorage.setItem("IPv6_Address", currentIPv6Address)
            }
        }
        if( if_newest === true ){
            // let badge_newest = document.getElementById("badge_newest_ipv6_address")
            let badge_newest = span_ipv6_address.getElementsByClassName("Badge_Newest").item(0)
            console.log(badge_newest!=null)
            badge_newest.removeAttribute("hidden")
        }
    }
    if( currentIPv6Prefix != null ){
        let code_ipv6_prefix = document.getElementById("code_ipv6_prefix")
        let status_icon_ipv6_prefix = document.getElementById("status_icon_ipv6_prefix")
        let if_newest = false
        // Show status
        if( code_ipv6_prefix.innerText === "None" ){
            console.log("[Warning]: code_ipv6_prefix is None")
            wrap_del_an_element(code_ipv6_prefix)
            status_icon_ipv6_prefix.style.background = "red"
        }
        else {
            status_icon_ipv6_prefix.style.background = "green"
            let storedIPv6Prefix = localStorage.getItem("IPv6_Prefix")
            if( storedIPv6Prefix !== currentIPv6Prefix ){
                console.log("[Info]: New IPv6_Prefix")
                if_newest = true
                // storedIPv6Prefix = currentIPv6Prefix
                localStorage.setItem("IPv6_Prefix", currentIPv6Prefix)
            }
        }
    }
    console.log("[checkNewestStatus]:End")
}

function checkNewestStatus_ver2(){
    console.log("[checkNewestStatus]:Begin")
    let span_ipv6_address = document.getElementById("span_ipv6_address")
    let span_ipv6_prefix = document.getElementById("span_ipv6_prefix")
    {
        // ipv6_address part
        let strdict = {}
        let logStringDict = {
            'code_item_is_none': "[Warning]: code_ipv6_address is None",
            'info_is_new': "[Info]: New IPv6_Address",
        }
        let storageKeyDict = {
            'key1': "IPv6_Address",
        }
        strdict['logStringDict'] = logStringDict
        strdict['storageKeyDict'] = storageKeyDict
        checkNewestStatus_ItemProcess_ProcessWithPattern(span_ipv6_address, strdict)
    }
    {
        // ipv6_prefix part
        let strdict = {}
        let logStringDict = {
            'code_item_is_none': "[Warning]: code_ipv6_prefix is None",
            'info_is_new': "[Info]: New IPv6_Prefix",
        }
        let storageKeyDict = {
            'key1': "IPv6_Prefix",
        }
        strdict['logStringDict'] = logStringDict
        strdict['storageKeyDict'] = storageKeyDict
        checkNewestStatus_ItemProcess_ProcessWithPattern(span_ipv6_prefix, strdict)
    }
    console.log("[checkNewestStatus]:End")
}

function checkNewestStatus_ItemProcess_ItemByClassName(item, strdict){
    // all is className, not ID. (deprecated)
    let classNameDict = strdict['classNameDict']
    let logStringDict = strdict['logStringDict']
    let storageKeyDict = strdict['storageKeyDict']
    let if_newest = false
    let code_item = item.getElementsByClassName(classNameDict['code_item_className'])[0]
    let status_icon_item = item.getElementsByClassName(classNameDict['status_icon_item_className'])[0]
    let info = code_item.innerText
    if( info === "None" ){
        console.log(logStringDict['code_item_is_none'])
        wrap_del_an_element(code_item)
        status_icon_item.style.background = "red"
    }
    else {
        status_icon_item.style.background = "green"
        let storedValue = localStorage.getItem(storageKeyDict['key1'])
        if( storedValue !== info ){
            console.log(logStringDict['info_is_new'])
            if_newest = true
            localStorage.setItem(storageKeyDict['key1'], info)
        }
    }
    if( if_newest === true ){
        let badge_newest = item.getElementsByClassName(classNameDict['badge_newest'])[0]
        // console.log(badge_newest!=null)
        badge_newest.item(0).removeAttribute("hidden")
    }
}

function checkNewestStatus_ItemProcess_ProcessWithPattern(item, strdict){
    let logStringDict = strdict['logStringDict']
    let storageKeyDict = strdict['storageKeyDict']
    let if_newest = false
    // let if_newest = true    // dev-opt
    let childNodes = item.childNodes
    let code_item
    let status_icon_item
    let badge_newest
    let info
    // get items part
    let i=0    // 共享index，顺序获取item。计数器不能共享。代码与顺序强关联。
    {
        // get status_icon_item
        for (let j=0,localName_index = 1; i<childNodes.length && j < localName_index; ++i){
            if( childNodes[i].localName === "span" ){
                ++j;
                if( j === localName_index ){
                    status_icon_item = childNodes[i]
                    break
                }
            }
        }
    }
    {
        // get code_item
        for (let j=0,localName_index = 1; i<childNodes.length && j < localName_index; ++i){
            if( childNodes[i].localName === "code" ){
                ++j;
                if( j === localName_index ){
                    code_item = childNodes[i]
                    break
                }
            }
        }
        {
            // get info
            info = code_item.innerText
        }
    }
    {
        // get badge_newest
        for (let j=0,localName_index = 1; i<childNodes.length && j < localName_index; ++i){
            if( childNodes[i].localName === "span" ){
                ++j;
                if( j === localName_index ){
                    badge_newest = childNodes[i]
                    break
                }
            }
        }
    }
    // Process Part
    if( info === "None" ){
        console.log(logStringDict['code_item_is_none'])
        wrap_del_an_element(code_item)
        status_icon_item.style.background = "red"
    }
    else {
        status_icon_item.style.background = "green"
        let storedValue = localStorage.getItem(storageKeyDict['key1'])
        if( storedValue !== info ){
            console.log(logStringDict['info_is_new'])
            if_newest = true
            localStorage.setItem(storageKeyDict['key1'], info)
        }
    }
    if( if_newest === true ){
        // console.log(badge_newest!=null)
        badge_newest.removeAttribute("hidden")
    }
}

// ________________ End of Part 2