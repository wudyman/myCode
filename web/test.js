function test1()
{
	var message=undefined;
	if(message)
	alert("true");
    else
	alert("false");
}
function test2()
{
alert(isNaN(true));
}
function test3()
{
	var num=100;
	num+=1;
	alert(num);
}
function test4()
{
	var val1="value1";
	var val2="value2";
	alert(val1&&val2);
}
function test5()
{
	alert(arguments[1]);
}
function test6()
{
	var person="wudy";
	person.age=32;
	alert(person.age);
}
function test7()
{
	var person=new Object();
	person.name="wudy";
	person.age=32;
	alert(person.age);
}
function test8()
{
	var name="Nicolas";
	var num=22;
	var b=true;
	var u; 
	var n=null;
	var person=new Object();
	alert(typeof name);
	alert(typeof num);
	alert(typeof b);
	alert(typeof u);
	alert(typeof n);
	alert(typeof person);
}
function test9()
{
	var name="Nicolas";
	var person=new Object();
	alert(name instanceof Object);//false
	alert(person instanceof Object);//true
}
function testA()
{
	for(var i=0;i<10;i++)
		alert("i="+i);
	alert("final i="+i);
}
function testB()
{
	var person=
	{
		"name":"nicolas",
		"age":"29",
		five:"5",
		
		displayName:function()
		{
			alert(this.name);
		},
	};
	person.displayName();
	alert(person.age);
	alert(person.five);
}
function testC(arg)
{
	alert(arg.age);
}
function testD()
{
	var colors1=new Array(3);
	var colors2=["red","green","blue"];
	//alert(colors2.length); //3
	//alert(colors2[0]);//red
	//alert(colors1[0]);//undefined
	//colors2[3]="brown";
	//alert(colors2.length);//4
	//alert(colors2[3]);//brown
	//alert(colors1 instanceof Array);//true
	//alert(Array.isArray(colors1));//true
	//alert(colors2.toString()); //red,green,blue
	//alert(colors2.valueOf());//red,green,blue
	//alert(colors2);//red,green,blue
	//alert(colors2.toLocaleString());//red,green,blue
	//alert(colors2.join("||"));//red||green||blue
	//alert(colors2.join());//red,green,blue
	
	//alert(colors2.pop());//blue  //stack method //LIFO
	//alert(colors2.shift());//red  //FIFO
	//alert(colors2.length); //1
	//colors2.push("black");
	//alert(colors2.length); //2
	
	alert(colors2.indexOf("green"));//1
	alert(colors2.lastIndexOf("blue"));//2
}
function testE()
{
	var numbers=[1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1];
	alert(numbers.some(function(value){return value>2;}));//true
	alert(numbers.every(function(value){return value>2;}));//false
	alert(numbers.filter(function(value){return value>2;}));//3,4,5,6,7,8,9,8,7,6,5,4,3
	alert(numbers.map(function(value){return value*2;}));//2,4,6,8,10,12,4,16,18,16,14,12,10,8,6,4,2
	alert(numbers.forEach(function(value){return value*2;})); //undefined  //no return value.
}
function testF()
{
	var aString=" aa bb cc abc";
	var pattern="\bb\gi";
	alert(pattern.exec(aString));
}
function test10()
{
	alert(arguments.callee);
	test11();
}
function test11()
{
	alert(test11.caller);
	alert(arguments.callee);
	alert(arguments.caller);//undefined
}
function test12()
{
	var s1="some test";
	s1.color="red";
	alert(s1.color);//undefined
	var s2=new String("some test");
	s2.color="red";
	alert(s2.color);//red
}
function test13()
{
	var book={
		_year:2004,
		edition:1
	};
	Object.defineProperty(book,"year",{
		get:function(){
			return this._year;
		},
		set:function(newValue){
			if(newValue>2004){
				this._year=newValue;
				this.edition+=newValue-2004;
			}
		}
	});
	book.year=2005;
	alert(book.edition);//2
	alert(book._year);//2005
	alert(book.year);//2005
	alert(book.year===book._year);//true
	
	var descriptor=Object.getOwnPropertyDescriptor(book,"_year");
	alert(descriptor.value);
	alert(descriptor.configurable);
}
function test14()
{
	function Person(){
	}
	Person.prototype.name="Nicholas";
	Person.prototype.age=29;
	Person.prototype.job="Software Enginner";
	Person.prototype.friends=["Shelby","Court"];
	Person.prototype.sayName=function(){
		alert(this.name);
	};
	var person1=new Person();
	var person2=new Person();
	person1.name="Greg";
	//alert(person1.name);//"Greg"
	//alert(person2.name);//"Nicholas"
	//delete person1.name;
	//alert(person1.name);//"Nicholas" 来自原型
	alert(person2.friends);//shelby,Court
	person1.friends.push("Van");
	alert(person2.friends);//shelby,Court,Van
	
	console.log(person1);
	for(var k in person1)
	{
		console.log(k);
	}
}
function test15()
{
	console.log("test15");
	goog={};
	goog=this;
	console.log(goog);//goog=window(include goog=window(include goog)...)
}
function test16()
{
	console.log("test16");
	window.addEventListener("load",test15,false);
}
function test17()
{
	for(var i = 0;i < 10;i++){
    (function(ii){
        setTimeout(function(){            
            console.log(ii);
        },1000);
    })(i);
  }
}
function test18()
{
	function consoleLog(i){  
	console.log(i);
	}
	for(var i = 0;i < 10;i++){
    setTimeout(consoleLog.bind(this,i),1000);
	}
}
function test19()
{
	var i;
	var j=100;
	function printMessage()
	{
		console.log(j);
		j--;
	}
	for(i = 0;i < 20;i++){
	console.log(i);
	setTimeout(printMessage,3000);
	}
}
function test20()
{
	id = 'window';
	//定义一个函数，但是不立即执行
	var test = function(){
    console.log(this.id)
	}
	test() // window
	//把test作为参数传递
	var obj = {
    id:'obj',
    hehe:test
	}
	//此时test函数运行环境发生了改变
	obj.hehe() // 'obj'
	//为了避免这种情况，javascript里面有一个bind方法可以在函数运行之前就绑定其作用域，修改如下
}
function test21()
{
	id = 'window';
	var test = function(){
    console.log(this.id)
	}.bind(this)
	var obj = {
    id:'obj',
    hehe:test
	}
	test() // window
	obj.hehe() // window
}
function test22()
{
	var obj1=new Promise();
	
	obj1.then(function(){
		console.log(this)});
}
function test23()
{
	function callbackF()
	{
		console.log("this is callbackF");
	}
	function callbackFA(i)
	{
		console.log("this is callbackFA"+i);
	}
	function test23_1(callback)
	{
		callback();
	}
	test23_1(callbackF);
	test23_1(function(){callbackFA("+arg");});
}
function test24()
{
	function callbackTest24(i)
	{
		console.log("this is callbackTest24"+i);
	}
	function test24_1(n,callback){
		callback(n);
	}
	test24_1("+arg2",callbackTest24);
}
function test25()
{
	function test25_1(callback)
	{
		callback();
	}
	test25_1(function(){console.log("this is callbackTest25");});
}
function test26()
{
	function test26_1(callback)
	{
		callback("+arg26");
	}
	test26_1(function(n){console.log("this is callbackTest26"+n);});
}
function test27()
{
    var foo=new Function("arg1","arg2","return arg1+arg2;");
	console.log(foo(2,3));
}
function test28()
{
	var foo=function(arg1,arg2){
		return arg1+arg2;
		}
	console.log(foo(2,3));
}
function test29()
{
	function callbackFoo(){
		console.log("this is callback");
	}
	function foo(callback){
		console.log("this is foo");
		callback();
	}
	foo(callbackFoo);
}
function test30()
{
	function foo(callback){
		console.log("this is foo");
		callback();
	}
	foo(function(){console.log("this is callback");});
}
function test31()
{
	function callbackFoo(n){
		console.log("this is callback,arg is:"+n);
	}
	function foo(arg,callback){
		console.log("this is foo");
		callback(arg);
	}
	foo(1,callbackFoo);
}
function test32()
{
	function callbackFoo(n){
		console.log("this is callback,arg is:"+n);
	}
	function foo(callback){
		console.log("this is foo");
		callback();
	}
	foo(function(){callbackFoo(2);});
}
function test33()
{
	var p = new Promise(function(resolve, reject) {
  
 // Do an async task async task and then...
 
	if(false) {
		console.log("resolve");
		resolve('Success!');
	}
	else {
		console.log("reject");
		reject('Failure!');
	}
	});
 
	p.then(function() { 
 /* do something with the result */
	console.log("sss");
	}).catch(function() {
 /* error */
 console.log("error");
	})
}
function test34()
{
	function f2(){
		console.log("this is f2");
	}
	function f1(callback){
		console.log("this is f1 a");
		setTimeout(function(){
		    console.log("this is f1 b");
			callback();},3000);
	}
	f1(f2);
	console.log("pending f1(f2);");
}
function test35()
{
	function f2(){
		console.log("this is f2");
	}
	function f1(){
		console.log("this is f1 a");
		var dfd = $.Deferred();
		setTimeout(function(){
		    console.log("this is f1 b");
			dfd.resolve();
			},3000);
		return dfd;
	}
	f1().then(f2);
	console.log("pending f1(f2);");
}
//testC({name:"nicolas",age:"27"});
function test36()
{
	function f2(){
		console.log("this is f2");
	}
	function f1(){
		console.log("this is f1 a");
		var p = new Promise(function(resolve,reject){
			setTimeout(function(){
				console.log("this is f1 b");
				resolve(20);
				},3000);
		});
		p.then(f2);
	}
	f1();
	console.log("pending f1(f2);");
}
function test37()
{
	var obj1={
	id:"obj1"
	};
	function f2(){
		console.log(this);
		console.log("this is f2");
	}
	function f1(){
		console.log("this is f1 a");
		console.log(this);
		var p = new Promise(function(resolve,reject){
			setTimeout(function(){
				console.log("this is f1 b");
				resolve(20);
				},3000);
		});
		return p;
	}
	f1.bind(obj1);//no use
	f1().then(f2);
	console.log("pending f1(f2);");
}
function test38()
{
	var obj1={
	id:"obj1"
	};
	function f3(){
		console.log("this is f3");
	}
	function f2(){
		console.log("this is f2");
	}
	function f1(){
		console.log("this is f1 a");
		//console.log(this);
		var p = Promise.resolve(); //implement f2
		//var p = Promise.reject(); //implement f3
		setTimeout(function(){
				console.log("this is f1 b");
				},3000);
		return p;
	}
    //f1().then(f2,f3);
	console.log(f1().then(f2,f3));
	console.log("pending f1().then(f2,f3);");
}
function test39()
{
	var outImg=document.getElementById("outputImage");
	//output.innerHTML = “<img src=\”” + url + “\”>”;
	outImg.innerHTML ="<img src=./img/shaka-player-init.png>";
	//var reader=new FileReader();
	//var xx=reader.readAsDataURL("./img/shaka-player-init.png");
    //console.log(xx);
}
function readFileByReader(file){ 
  if( file.size > 5*1024*1024 ){  //用size属性判断文件大小不能超过5M 
    alert( "你上传的文件太大了！" ) 
  }else{ 
    var reader = new FileReader(); 
    reader.readAsDataURL(file); 
    reader.onload = function(e){ 
    var res = this.result; 
    $("#Img").attr("src", res); 
    } 
  }
} 
function readFileByBlob(file){ 
  if( file.size > 5*1024*1024 ){  //用size属性判断文件大小不能超过5M 
    alert( "你上传的文件太大了！" ) 
  }else{ 
	 url = window.URL.createObjectURL(file);
	 $("#Img").attr("src", url);
    } 
} 
function readFile()
{
	var file = this.files[0]; //input 
	//readFileByBlob(file);
	readFileByReader(file);
}
function test40()
{
	document.getElementById("idFile").addEventListener("change", readFile, false); 
}
function test41(){
	console.log(window);
	console.log(location);
	console.log(navigator);
	console.log(history);
	//window.resizeTo(100,100);
	//window.open("https://www.baidu.com","_blank");
}
function test42(){
	function showXY()
	{
		console.log("x="+event.clientX+",y="+event.clientY);
	}
	var v1=document.getElementById("id1");
	v1.addEventListener("click",showXY,false);
}
function test43()
{
    var html='<div><p>ssssssssssssssssssssssssssssssssssssssss</p><p>xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx</p><p>1111111111111111111111111111111111</p><p>22222222222222222222222222222222</p><p>444444444444444444444444444444</p><p>5555555555555555555555555555555</p><p>666666666666666666666666666666</p><p>7777777777777777777777777777777777777777777777777777</p><p>8888888888888888888888888888888888888888</p><p>9999999999999999999999999999999999999999999</p><p>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa<img src="/media/img/wudy1510882997.jpg" data-filename="image name" style="width: 728px;"></p><p><br></p><p><br></p><p><br></p><p><br></p><p><br></p><p>ddddddddddddddddddddddddddddddddddddddddddd</p><p>ssssssssssssssssssssssssssssssssssssssssssssssssss</p><p>fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff</p><p><img src="/media/img/wudy1510883020.jpg" data-filename="image name" style="width: 728px;"></p><p><br></p><p><br></p><p>ddddddddddddddddd</p><p>wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww</p></div>';
    var imgReg=/<img.*?(?:>|\/>)/gi;
    var arr=html.match(imgReg);
    html2=html.replace(imgReg,"");
    var srcReg = /src=[\'\"]?([^\'\"]*)[\'\"]?/i;
    src0=arr[0].match(srcReg);
    alert(src0[1]);
    alert(arr[0]);
    alert(html2);
    
}
function test44()
{
    alert("test44");
    var f1=function(){alert("f1")};
    f1();
}
function test45()
{
    var x=[15];
    y=15;
    if(x.indexOf(y)==-1)
        alert("false");
    else
        alert("success");
}
function test46()
{
    x=1;
    y=2;
    z=3;
    console.log(z);
}
test46();

//alert(message);