function gapiLoaded() {
  const API_KEY = 'AIzaSyCtdsxq4_TWBoQU-gZEiA6YVQZUaweN6C8'; //CHANGE
  const DISCOVERY_DOC = 'https://sheets.googleapis.com/$discovery/rest?version=v4';
  gapi.load('client', async () => {
      await gapi.client.init({
          apiKey: API_KEY,
          discoveryDocs: [DISCOVERY_DOC],
      });
      get_teams();
  });
}

//issue? We need to reload the page, each time we make a change to the google sheet 
async function get_teams() {
  try {
    // fetching the 1 line 
    response = await gapi.client.sheets.spreadsheets.values.get({
      spreadsheetId: '1c9NUoB1prQdrBfAAkaSKJCnIGrAQV8kx5GZKEeIAmWs',
      range: 'Inspection!A2:C7',
    });
    console.log('t', response) //prints shows the spreadsheet values 
  } catch (err) {
    console.log("NOT WORKING")

    document.getElementById('content').innerText = err.message;
    return;
  }
    //Getting Everything from Google SHeet 
      //1. make two arrays - one for blue and yello box =-
      //2. get the ranges for blu queue. 

  game_data = response.result.values

  console.log('here is the array', game_data) //printing the range 
  console.log('index show', game_data.at(0)) //printing the first one 

  //EX:
  //document.getElementById('que1').innerHTML = game_data.at(0).at(0); //this places the game_data into the first label 


  for (let i = 0; i < game_data.length; i++) {
    //we are printing for each row 
    row = game_data.at(i); //this is the first row 
    document.getElementById('que'+ String(i)).innerHTML = row.at(0); //this places the game_data into the first input
    document.getElementById('insp'+ String(i)).innerHTML = row.at(1);
    document.getElementById('play'+ String(i)).innerHTML = row.at(2);
}
}

//function to keep refreshing 

setInterval('get_teams()', 1000);


//DELETE HERE
async function listMajors() {
  try {
    // fetching the 1 line 
    response = await gapi.client.sheets.spreadsheets.values.get({
      spreadsheetId: '1c9NUoB1prQdrBfAAkaSKJCnIGrAQV8kx5GZKEeIAmWs',
      range: 'Inspection!A2:A5',
    });
    console.log(response)
  } catch (err) {
    document.getElementById('content').innerText = err.message;
    //document.getElementById('content').innerText = err.message;
    return;
  }

  const output = range.values.reduce(
    (str, row) => `${str}${row[0]}, ${row[4]}\n`,
    'Name, Major:\n');
  document.getElementById('content').innerText = output;

  console.log(game_data)
}



/* 
//GOOGLE SHEET
function getSheep(){
  return SpreadsheetApp.openById('1FtbpxMN9mF1hbZNHS1_ASNrEOf5wIKpRxvI_hHL3gtk').getSheetByName('Sheet41');
  //important: change if moving this file or if renaming the sheet
}

function doPost(e) {  
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) {
    Logger.log('Lock not obtained: '+new Date().toUTCString());
    return HtmlService.createHtmlOutput("failure").setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  }
  
  var sheep = getSheep();
  var row = sheep.getLastRow()+1;
  
  if(typeof e !== 'undefined'){
    sheep.getRange(row,  1).setValue(new Date().toLocaleString('en-US', { timeZone: 'Pacific' }));
    sheep.getRange(row,  2).setValue(e.parameter.data);
  }
  
  lock.releaseLock();
  return HtmlService.createHtmlOutput("success").setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
 
 */
 