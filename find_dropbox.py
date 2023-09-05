import dropbox
  
# oken Generated from dropbox
TOKEN = "sl.Bi1JnK55Cf3vJk4iWaELCikvwyZlvNKt0AJzVhAKAgifzRcDmE8z7wTCCb8Hyevb3CShxTuH75ZVUHz6LBBk5v-sYwpz_C-3PpVuDqYxijUt9oa3BjZZeF32GvUCL-DWrsH1zk56HrZu"
  
#Establish connection
def connect_to_dropbox():
    
    try:
        dbx = dropbox.Dropbox(TOKEN)
        print('Connected to Dropbox successfully')
      
    except Exception as e:
        print(str(e))
      
    return dbx
  
#explicit function to list files
def list_files_in_folder():
    
    #dbx is passed in from the connect_to_dropbox function
    dbx = connect_to_dropbox()
      
    try:
        folder_path = "/Jack Burns"
  
        files = dbx.files_list_folder(folder_path).entries
        print("------------Listing Files in Folder------------ ")
          
        for file in files:
              
            #print for now.
            print(file.name)
              
    except Exception as e:
        print(str(e))


dbx = connect_to_dropbox()
list_files_in_folder()