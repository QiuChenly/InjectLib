#!/bin/zsh

/usr/bin/logger "Starting Office for Mac License Removal 2.7"

## CONSTANTS
PERPLICENSE="/Library/Preferences/com.microsoft.office.licensingV2.plist"
PERPLICENSEBACKUP="/Library/Preferences/com.microsoft.office.licensingV2.Backup"

## FUNCTIONS
GetLoggedInUser() {
	LOGGEDIN=$(/bin/echo "show State:/Users/ConsoleUser" | /usr/sbin/scutil | /usr/bin/awk '/Name :/&&!/loginwindow/{print $3}')
	if [ "$LOGGEDIN" = "" ]; then
		echo "$USER"
	else
		echo "$LOGGEDIN"
	fi
}

SetHomeFolder() {
	HOME=$(dscl . read /Users/"$1" NFSHomeDirectory | cut -d ':' -f2 | cut -d ' ' -f2)
	if [ "$HOME" = "" ]; then
		if [ -d "/Users/$1" ]; then
			HOME="/Users/$1"
		else
			HOME=$(eval echo "~$1")
		fi
	fi
}

GetNodeId() {
# Get node_id value from Registry
	local NAME="$1"
	local PARENT="$2"
	local NODEVALUE=$(sqlite3 "$REGISTRY" "SELECT node_id from HKEY_CURRENT_USER WHERE name='$NAME' AND parent_id=$PARENT;")
	if [ "$NODEVALUE" == '' ]; then
		echo "0"
	else
		echo "$NODEVALUE"
	fi
}

GetNodeVal() {
# Get node value from Registry
	local NAME="$1"
	local NODEID="$2"
	local NODEVALUE=$(sqlite3 "$REGISTRY" "SELECT node_id from HKEY_CURRENT_USER_values WHERE name='$NAME' AND parent_id=$NODEID;")
	if [ "$NODEVALUE" == '' ]; then
		echo "0"
	else
		echo "$NODEVALUE"
	fi
}

DeleteValue() {
# Delete value from Registry
	local NAME="$1"
	local NODEID="$2"
	sqlite3 "$REGISTRY" "DELETE FROM HKEY_CURRENT_USER_values WHERE name='$NAME' and node_id=$NODEID;"
}

NukeValue() {
# Delete value from Registry with just the node name
	local NAME="$1"
	sqlite3 "$REGISTRY" "DELETE FROM HKEY_CURRENT_USER_values WHERE name='$NAME';"
}

DeleteNode() {
# Delete node and all contained values from Registry
	local NODEID="$1"
	sqlite3 "$REGISTRY" "DELETE FROM HKEY_CURRENT_USER_values WHERE node_id=$NODEID;"
}

RemoveFlightData() {
# Remove all flighting keys from the specified app
	local KEY_APP="$1"
	# If the flight keys are set, remove the existing values
	KEY_ETAG=($GetNodeVal "ETag" "$KEY_APP")
	if [ "$KEY_ETAG" != "0" ]; then
		DeleteValue "ETag" "$KEY_APP"
	fi
	KEY_EXPIRES=($GetNodeVal "Expires" "$KEY_APP")
	if [ "$KEY_EXPIRES" != "0" ]; then
		DeleteValue "Expires" "$KEY_APP"
	fi
	KEY_DEFERRED=($GetNodeVal "DeferredConfigs" "$KEY_APP")
	if [ "$KEY_DEFERRED" != "0" ]; then
		DeleteValue "DeferredConfigs" "$KEY_APP"
	fi
	KEY_CONFIGID=($GetNodeVal "ConfigIds" "$KEY_APP")
	if [ "$KEY_CONFIGID" != "0" ]; then
		DeleteValue "ConfigIds" "$KEY_APP"
	fi
}

## MAIN
LoggedInUser=$(GetLoggedInUser)
SetHomeFolder "$LoggedInUser"
echo "Running as: $LoggedInUser; Home Folder: $HOME"

REGISTRY="$HOME/Library/Group Containers/UBF8T346G9.Office/MicrosoftRegistrationDB.reg"
O365SUBMAIN="$HOME/Library/Group Containers/UBF8T346G9.Office/com.microsoft.Office365.plist"
O365SUBBAK1="$HOME/Library/Group Containers/UBF8T346G9.Office/com.microsoft.e0E2OUQxNUY1LTAxOUQtNDQwNS04QkJELTAxQTI5M0JBOTk4O.plist"
O365SUBBAK2="$HOME/Library/Group Containers/UBF8T346G9.Office/e0E2OUQxNUY1LTAxOUQtNDQwNS04QkJELTAxQTI5M0JBOTk4O"
O365SUBMAINB="$HOME/Library/Group Containers/UBF8T346G9.Office/com.microsoft.Office365V2.plist"
O365SUBBAK1B="$HOME/Library/Group Containers/UBF8T346G9.Office/com.microsoft.O4kTOBJ0M5ITQxATLEJkQ40SNwQDNtQUOxATL1YUNxQUO2E0e.plist"
O365SUBBAK2B="$HOME/Library/Group Containers/UBF8T346G9.Office/O4kTOBJ0M5ITQxATLEJkQ40SNwQDNtQUOxATL1YUNxQUO2E0e"
O365PRODUCT="$HOME/Library/Group Containers/UBF8T346G9.Office"
VNEXTLICENSEPATH="$O365PRODUCT/Licenses"
VNEXTPERPETUALLICENSEPATH="/Library/Microsoft/Office/Licenses"

# Forcibly close Office apps if they are running
/usr/bin/pkill -HUP "Microsoft Word"
/usr/bin/pkill -HUP "Microsoft Excel"
/usr/bin/pkill -HUP "Microsoft PowerPoint"
/usr/bin/pkill -HUP "Microsoft Outlook"
/usr/bin/pkill -HUP "Microsoft OneNote"

# Remove the Perpetual/Volume License from the computer
if [ -f "$PERPLICENSE" ]
then
	/usr/bin/logger "Detected $PERPLICENSE file"
	/usr/bin/sudo mv -f "$PERPLICENSE" "$PERPLICENSEBACKUP"
	/usr/bin/logger "Removed $PERPLICENSE file"
else
	/usr/bin/logger "Did NOT detect $PERPLICENSE file"
fi

# Remove the 2021 Consumer Perpetual Licence from the computer
if [ -e "$VNEXTPERPETUALLICENSEPATH" ]
then
	/usr/bin/logger "Detected $VNEXTPERPETUALLICENSEPATH folder"
	/usr/bin/sudo rm -rf "$VNEXTPERPETUALLICENSEPATH"
	/usr/bin/logger "Removed $VNEXTPERPETUALLICENSEPATH folder"
else
	/usr/bin/logger "Did NOT detect $VNEXTPERPETUALLICENSEPATH folder"
fi

# Remove the Office 365 Subscription License
if [ -f "$O365SUBMAIN" ] || [ -f "$O365SUBBAK1" ] || [ -f "$O365SUBBAK2" ] || [ -f "$O365SUBMAINB" ] || [ -f "$O365SUBBAK1B" ] || [ -f "$O365SUBBAK2B" ] || [ -e "$VNEXTLICENSEPATH" ]
then
	/bin/logger "Detected Office 365 Subscription License file"
	/bin/rm -f "$O365SUBMAIN"
	/bin/rm -f "$O365SUBBAK1"
	/bin/rm -f "$O365SUBBAK2"
	/bin/rm -f "$O365SUBMAINB"
	/bin/rm -f "$O365SUBBAK1B"
	/bin/rm -f "$O365SUBBAK2B"
	/bin/rm -rf "$VNEXTLICENSEPATH"
	/usr/bin/logger "Removed all Office 365 Subscription License files"
else
	/usr/bin/logger "Did NOT detect Office 365 Subscription License file"
fi

KeychainHasLogin=$(/usr/bin/security list-keychains | grep 'login.keychain')
if [ "$KeychainHasLogin" = "" ]; then
	echo "Adding user login keychain to list"
	/usr/bin/security list-keychains -s "$HOME/Library/Keychains/login.keychain-db"
fi

echo "Display list-keychains for logged-in user"
/usr/bin/security list-keychains

# Remove any keychain entries for Office
/usr/bin/security delete-generic-password -s 'OneAuthAccount'
/usr/bin/security delete-internet-password -s 'msoCredentialSchemeADAL'
/usr/bin/security delete-internet-password -s 'msoCredentialSchemeLiveId'
/usr/bin/security delete-generic-password -l 'Microsoft Office Identities Settings 2'
/usr/bin/security delete-generic-password -l 'Microsoft Office Identities Settings 3'
/usr/bin/security delete-generic-password -l 'Microsoft Office Identities Cache 2'
/usr/bin/security delete-generic-password -l 'Microsoft Office Identities Cache 3'
/usr/bin/security delete-generic-password -l 'Microsoft Office Ticket Cache'
/usr/bin/security delete-generic-password -l 'com.microsoft.adalcache'
/usr/bin/security delete-generic-password -l 'com.microsoft.OutlookCore.Secret'
/usr/bin/security delete-generic-password -l 'MicrosoftOfficeRMSCredential'
/usr/bin/security delete-generic-password -l 'MSProtection.framework.service'
/usr/bin/security delete-generic-password -G 'MSOpenTech.ADAL.1'
/usr/bin/security delete-generic-password -G 'MSOpenTech.ADAL.1'
/usr/bin/security delete-generic-password -G 'Microsoft Office Data'
/usr/bin/security delete-generic-password -G 'Microsoft Office Data'
/usr/bin/security delete-generic-password -G 'Microsoft Office Data'
/usr/bin/security delete-generic-password -l 'com.microsoft.OutlookCore.Secret'
/usr/bin/security delete-generic-password -l 'com.helpshift.data_com.microsoft.Outlook'
/usr/bin/security delete-generic-password -l 'com.helpshift.data_com.microsoft.Outlook'
/usr/bin/security delete-generic-password -l 'com.helpshift.data_com.microsoft.Outlook'
/usr/bin/security delete-generic-password -l 'com.helpshift.data_com.microsoft.Outlook'
/usr/bin/security delete-generic-password -l 'MicrosoftOfficeRMSCredential'
/usr/bin/security delete-generic-password -l 'MicrosoftOfficeRMSCredential'
/usr/bin/security delete-generic-password -l 'MSProtection.framework.service'
/usr/bin/security delete-generic-password -l 'MSProtection.framework.service'
/usr/bin/logger "Removed all Office keychain entries"

# Remove the Belongs To information
if [ -e "$HOME/Library/Preferences/com.microsoft.office.plist" ]; then
	/usr/bin/sudo -u $LoggedInUser /usr/bin/defaults delete $HOME/Library/Preferences/com.microsoft.office OfficeActivationEmailAddress
	/usr/bin/sudo -u $LoggedInUser /usr/bin/defaults write $HOME/Library/Preferences/com.microsoft.office OfficeAutoSignIn -bool TRUE
	/usr/bin/sudo -u $LoggedInUser /usr/bin/defaults write $HOME/Library/Preferences/com.microsoft.office HasUserSeenFREDialog -bool TRUE
	/usr/bin/sudo -u $LoggedInUser /usr/bin/defaults write $HOME/Library/Preferences/com.microsoft.office HasUserSeenEnterpriseFREDialog -bool TRUE
fi

# Reset the first run experience for each licensed app
if [ -e "$HOME/Library/Containers/com.microsoft.Word/Data/Library/Preferences/com.microsoft.Word.plist" ]; then
	/usr/bin/sudo -u $LoggedInUser /usr/bin/defaults write $HOME/Library/Containers/com.microsoft.Word/Data/Library/Preferences/com.microsoft.Word kSubUIAppCompletedFirstRunSetup1507 -bool FALSE
fi
if [ -e "$HOME/Library/Containers/com.microsoft.Excel/Data/Library/Preferences/com.microsoft.Excel.plist" ]; then
	/usr/bin/sudo -u $LoggedInUser /usr/bin/defaults write $HOME/Library/Containers/com.microsoft.Excel/Data/Library/Preferences/com.microsoft.Excel kSubUIAppCompletedFirstRunSetup1507 -bool FALSE
fi
if [ -e "$HOME/Library/Containers/com.microsoft.Powerpoint/Data/Library/Preferences/com.microsoft.Powerpoint.plist" ]; then
	/usr/bin/sudo -u $LoggedInUser /usr/bin/defaults write $HOME/Library/Containers/com.microsoft.Powerpoint/Data/Library/Preferences/com.microsoft.Powerpoint kSubUIAppCompletedFirstRunSetup1507 -bool FALSE
fi
if [ -e "$HOME/Library/Containers/com.microsoft.Outlook/Data/Library/Preferences/com.microsoft.Outlook.plist" ]; then
	/usr/bin/sudo -u $LoggedInUser /usr/bin/defaults write $HOME/Library/Containers/com.microsoft.Outlook/Data/Library/Preferences/com.microsoft.Outlook kSubUIAppCompletedFirstRunSetup1507 -bool FALSE
fi
if [ -e "$HOME/Library/Containers/com.microsoft.onenote.mac/Data/Library/Preferences/com.microsoft.onenote.mac.plist" ]; then
	/usr/bin/sudo -u $LoggedInUser /usr/bin/defaults write $HOME/Library/Containers/com.microsoft.onenote.mac/Data/Library/Preferences/com.microsoft.onenote.mac kSubUIAppCompletedFirstRunSetup1507 -bool FALSE
fi

/usr/bin/logger "Set apps back to first run state"

# Remove the current flights from the registry
KEY_SOFTWARE=$(GetNodeId "Software" '-1')
KEY_MICROSOFT=$(GetNodeId "Microsoft" "$KEY_SOFTWARE")
KEY_OFFICE=$(GetNodeId "Office" "$KEY_MICROSOFT")
KEY_VERSION=$(GetNodeId "16.0" "$KEY_OFFICE")
KEY_COMMON=$(GetNodeId "Common" "$KEY_VERSION")
KEY_ECS=$(GetNodeId "ExperimentEcs" "$KEY_COMMON")
KEY_WORD=$(GetNodeId "word" "$KEY_ECS")
KEY_WORD_FLIGHTS=$(GetNodeId "Flights" "$KEY_WORD")
KEY_EXCEL=$(GetNodeId "excel" "$KEY_ECS")
KEY_EXCEL_FLIGHTS=$(GetNodeId "Flights" "$KEY_EXCEL")
KEY_POWERPOINT=$(GetNodeId "powerpoint" "$KEY_ECS")
KEY_POWERPOINT_FLIGHTS=$(GetNodeId "Flights" "$KEY_POWERPOINT")
KEY_OUTLOOK=$(GetNodeId "outlook" "$KEY_ECS")
KEY_OUTLOOK_FLIGHTS=$(GetNodeId "Flights" "$KEY_OUTLOOK")
KEY_ONENOTE=$(GetNodeId "onenote" "$KEY_ECS")
KEY_ONENOTE_FLIGHTS=$(GetNodeId "Flights" "$KEY_ONENOTE")
KEY_LICENSING=$(GetNodeId "licensingdaemon" "$KEY_ECS")
KEY_LICENSING_FLIGHTS=$(GetNodeId "Flights" "$KEY_LICENSING")

KEY_EX_CONFIGS=$(GetNodeId "ExperimentConfigs" "$KEY_COMMON")
KEY_EX_ECS=$(GetNodeId "Ecs" "$KEY_EX_CONFIGS")
KEY_EX_ECS_WORD=$(GetNodeId "word" "$KEY_EX_ECS")
KEY_EX_ECS_WORD_CCD=$(GetNodeId "ConfigContextData" "$KEY_EX_ECS_WORD")
KEY_EX_ECS_EXCEL=$(GetNodeId "excel" "$KEY_EX_ECS")
KEY_EX_ECS_EXCEL_CCD=$(GetNodeId "ConfigContextData" "$KEY_EX_ECS_EXCEL")
KEY_EX_ECS_POWERPOINT=$(GetNodeId "powerpoint" "$KEY_EX_ECS")
KEY_EX_ECS_POWERPOINT_CCD=$(GetNodeId "ConfigContextData" "$KEY_EX_ECS_POWERPOINT")
KEY_EX_ECS_OUTLOOK=$(GetNodeId "outlook" "$KEY_EX_ECS")
KEY_EX_ECS_OUTLOOK_CCD=$(GetNodeId "ConfigContextData" "$KEY_EX_ECS_OUTLOOK")
KEY_EX_ECS_ONENOTE=$(GetNodeId "onenote" "$KEY_EX_ECS")
KEY_EX_ECS_ONENOTE_CCD=$(GetNodeId "ConfigContextData" "$KEY_EX_ECS_ONENOTE")
KEY_EX_ECS_LICENSING=$(GetNodeId "licensingdaemon" "$KEY_EX_ECS")
KEY_EX_ECS_LICENSING_CCD=$(GetNodeId "ConfigContextData" "$KEY_EX_ECS_LICENSING")

RemoveFlightData "$KEY_WORD"
RemoveFlightData "$KEY_EX_ECS_WORD"
DeleteNode "$KEY_WORD_FLIGHTS"
DeleteNode "$KEY_EX_ECS_WORD_CCD"
RemoveFlightData "$KEY_EXCEL"
RemoveFlightData "$KEY_EX_ECS_EXCEL"
DeleteNode "$KEY_EXCEL_FLIGHTS"
DeleteNode "$KEY_EX_ECS_EXCEL_CCD"
RemoveFlightData "$KEY_POWERPOINT"
RemoveFlightData "$KEY_EX_ECS_POWERPOINT"
DeleteNode "$KEY_POWERPOINT_FLIGHTS"
DeleteNode "$KEY_EX_ECS_POWERPOINT_CCD"
RemoveFlightData "$KEY_OUTLOOK"
RemoveFlightData "$KEY_EX_ECS_OUTLOOK"
DeleteNode "$KEY_OUTLOOK_FLIGHTS"
DeleteNode "$KEY_EX_ECS_OUTLOOK_CCD"
RemoveFlightData "$KEY_ONENOTE"
RemoveFlightData "$KEY_EX_ECS_ONENOTE"
DeleteNode "$KEY_ONENOTE_FLIGHTS"
DeleteNode "$KEY_EX_ECS_ONENOTE_CCD"
RemoveFlightData "$KEY_LICENSING"
RemoveFlightData "$KEY_EX_ECS_LICENSING"
DeleteNode "$KEY_LICENSING_FLIGHTS"
DeleteNode "$KEY_EX_ECS_LICENSING_CCD"
/usr/bin/logger "Removed all Office flighting data"

# Forcibly remove any Config Service Caching
NukeValue "AuthorityUrl"
NukeValue "FilePath"
NukeValue "Url"

# Restart the CFPreferences daemon to ensure that all caches are flushed
/usr/bin/sudo /usr/bin/killall cfprefsd
/usr/bin/logger "Terminated all instances of CFPrefsd"

/usr/bin/logger "Completed Office for Mac License Removal 2.7"

exit 0