function gapiLoaded() {
  const API_KEY = 'AIzaSyB5cHv1n6pMZ326cG_jGUhbgadmIB8KBkI';
  const DISCOVERY_DOC = 'https://sheets.googleapis.com/$discovery/rest?version=v4';
  gapi.load('client', async () => {
      await gapi.client.init({
          apiKey: API_KEY,
          discoveryDocs: [DISCOVERY_DOC],
      });
      getBlueQueue();
  });
}
async function getBlueQueue() {
  try {
    // fetching the 1 line 
    response = await gapi.client.sheets.spreadsheets.values.get({
      spreadsheetId: '1FtbpxMN9mF1hbZNHS1_ASNrEOf5wIKpRxvI_hHL3gtk',
      range: 'Inspection!A2:A5',
    });

    console.log('t', response) //prints shows the spreadsheet values 
  } catch (err) {
    console.log(err.message)
    //document.getElementById('content').innerText = err.message;
    return;
  }

  game_data = response.result.values

  console.log('here is the array', game_data) //printing the range 
  console.log('index show', game_data.at(0)) //printing the first one 
}



async function listMajors() {
  try {
    // fetching the 1 line 
    response = await gapi.client.sheets.spreadsheets.values.get({
      spreadsheetId: '1FtbpxMN9mF1hbZNHS1_ASNrEOf5wIKpRxvI_hHL3gtk',
      range: 'Inspection!A2:A5',
    });
    console.log(response)
  } catch (err) {
    console.log(err.message)
    //document.getElementById('content').innerText = err.message;
    return;
  }

  game_data = response.result.values

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
 