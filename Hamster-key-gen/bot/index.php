<?php
header("Cache-Control: no-cache, must-revalidate");
header("Pragma: no-cache");
header("Expires: 0");

date_default_timezone_set('Asia/Tehran');
ini_set("log_errors", "off");
error_reporting(0);


$DB = [
'dbname' => 'xxxxxxxxxxxxxxxxx',
'username' => 'xxxxxxxxxxxxxxxxx',
'password' => 'xxxxxxxxxxxxxxxxx'
];


$MySQLi = new mysqli('localhost',$DB['username'],$DB['password'],$DB['dbname']);
$MySQLi->query("SET NAMES 'utf8'");
$MySQLi->set_charset('utf8mb4');
if ($MySQLi->connect_error) die;
function ToDie($MySQLi){
$MySQLi->close();
die;
}

$query = "CREATE TABLE IF NOT EXISTS users (
id BIGINT(255) PRIMARY KEY,
step VARCHAR(255) DEFAULT NULL
) default charset = utf8mb4";
$MySQLi->query($query);
$query = "CREATE TABLE IF NOT EXISTS sending (
type VARCHAR(255) PRIMARY KEY,
chat_id BIGINT(255) DEFAULT NULL,
msg_id BIGINT(255) DEFAULT NULL,
count BIGINT(225) DEFAULT NULL
) default charset = utf8mb4";
$MySQLi->query($query);


$apiKey = '7375484841:xxxxxxxxxxxxxxxxxxxxxxxx';


$web_app = 'https://xxxxxxxx.com/HamsterKeyGen/index.html';


$LockChannelsUserName = [
"https://t.me/+2Q65Z_EfLdoyY2Jk",
];
$LockChannelsUserID = [
-1001478594200,
];
$LockChannelsNames = [
'osClub',
];


function LampStack($method,$datas=[]){
global $apiKey;
$url = 'https://api.telegram.org/bot'.$apiKey.'/'.$method;
$ch = curl_init();
curl_setopt($ch,CURLOPT_URL,$url);
curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
curl_setopt($ch,CURLOPT_POSTFIELDS,$datas);
$res = curl_exec($ch);
if(curl_error($ch)){
return json_decode(curl_error($ch));
}else{
return json_decode($res);
}
}

function joinCheck($uid){
global $LockChannelsUserID;
global $apiKey;
$chArr = [];
foreach($LockChannelsUserID as $value){
$chArr[] = json_decode(file_get_contents('https://api.telegram.org/bot'.$apiKey.'/getChatMember?chat_id='.$value.'&user_id='.$uid))->result->status;
}
if(in_array('left', $chArr)) return false;
return true;
}

$update = json_decode(file_get_contents('php://input'));
if(isset($update->message)) {
@$msg = $update->message->text;
@$chat_id = $update->message->chat->id;
@$from_id = $update->message->from->id;
@$first_name = $update->message->from->first_name;
@$last_name = $update->message->from->last_name?:null;
@$username = $update->message->from->username?:null;
@$is_premium = $update->message->from->is_premium;
@$language_code = $update->message->from->language_code?:'en';
@$chat_type = $update->message->chat->type;
@$message_id = $update->message->message_id;
@$reply_message_id = $update->message->reply_to_message->message_id?:null;
$isHeJoined = joinCheck($from_id);
}

if(isset($update->callback_query)) {
@$callback_query_data = $update->callback_query->data;
@$chat_id = $update->callback_query->message->chat->id;
@$from_id = $update->callback_query->from->id;
@$chat_type = $update->callback_query->message->chat->type;
@$message_id = $update->callback_query->message->message_id;
@$name = $update->callback_query->from->first_name;
@$username = $update->callback_query->from->username?:null;
$isHeJoined = joinCheck($from_id);
}

$UserDataBase = mysqli_fetch_assoc(mysqli_query($MySQLi, "SELECT * FROM `users` WHERE `id` = '{$from_id}' LIMIT 1"));
if(!$UserDataBase){
$MySQLi->query("INSERT INTO `users` (`id`) VALUES ('{$from_id}')");
}

        //  users join checking           //
if($isHeJoined == false){
if(isset($update->message)) {
for($i=0; $i<count($LockChannelsUserName); $i++){
$d4[] = [['text'=>$LockChannelsNames[$i],'url'=>$LockChannelsUserName[$i]]];
}
$d4[] = [['text'=>'Joined ✅','callback_data'=>'BackToMainMenu']];
LampStack('sendMessage',[
'chat_id'=>$from_id,
'text'=> "To use the robot, first subscribe to the channels below👇🏻",
'parse_mode'=>"HTML",
'reply_markup'=>json_encode([
'inline_keyboard'=>$d4
])
]);
}
if(isset($update->callback_query)) {
LampStack('answercallbackquery', [
'callback_query_id' => $update->callback_query->id,
'text' => 'To use the robot, you must join the channels sponsored by the robot.',
'show_alert' => true
]);
}
$MySQLi->close();
die;
}

if($callback_query_data === 'BackToMainMenu'){
LampStack('deleteMessage',[
'chat_id' => $from_id,
'message_id' => $message_id,
]);
LampStack('sendPhoto',[
'chat_id' => $from_id,
'photo' => new CURLFILE('home.jpg'),
'caption' => '
Hi, welcome to Hamster Kombat Key generating bot.

With this bot, you can get unlimited Hamster games key for free and without referral.

Developer : @LampStack
',
'parse_mode' => 'HTML',
'reply_markup' => json_encode([
'inline_keyboard' => [
[['text' => 'Generate Keys 🔑', 'web_app' => ['url' => $web_app]]],
]
])
]);
$MySQLi->close();
die;
}


if($msg === '/start'){
LampStack('sendPhoto',[
'chat_id' => $from_id,
'photo' => new CURLFILE('home.jpg'),
'caption' => '
Hi, welcome to Hamster Kombat Key generating bot.

With this bot, you can get unlimited Hamster games key for free and without referral.

Developer : @LampStack
',
'parse_mode' => 'HTML',
'reply_to_message_id' => $message_id,
'reply_markup' => json_encode([
'inline_keyboard' => [
[['text' => 'Generate Keys 🔑', 'web_app' => ['url' => $web_app]]],
]
])
]);
$MySQLi->close();
die;
}