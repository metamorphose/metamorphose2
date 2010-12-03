;Based on :
;Welcome/Finish Page Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI.nsh"

;--------------------------------
;General

  ;Name and file
  !define VERSION "0.7.1"

  Name "Métamorphose2"
  OutFile "metamorphose2_${VERSION}_setup.exe"
  !define MUI_ICON "metsetup.ico"
  !define MUI_UNICON "metsetup.ico"
  !define MUI_WELCOMEFINISHPAGE_BITMAP "wizard_i.bmp"
  !define MUI_UNWELCOMEFINISHPAGE_BITMAP "wizard_u.bmp"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKLM "Software\metamorphose2" ""

  ;Default installation folder
  InstallDir "$PROGRAMFILES\metamorphose2"

  VIProductVersion "2.0.7.1"
  VIAddVersionKey "ProductName" "Métamorphose2"
  VIAddVersionKey "CompanyName" "Ianaré Sévi"
  VIAddVersionKey "LegalCopyright" "(C) 2006-2009 Ianaré Sévi"
  VIAddVersionKey "FileDescription" "Installer for Métamorphose 2.${VERSION}"
  VIAddVersionKey "FileVersion" "${VERSION}"

  !define CSIDL_SYSTEM "0x25" ;System path

  XPStyle on
  SetCompressor /SOLID lzma
  
  ;Request application privileges for Windows Vista / 7
  RequestExecutionLevel admin

;--------------------------------
;Variables

  Var MUI_TEMP
  Var STARTMENU_FOLDER

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING
  !define MUI_COMPONENTSPAGE_CHECKBITMAP "checks.bmp"

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "License.rtf"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  ;Start Menu Folder Page Configuration
  ;!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKLM"
  ;!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\metamorphose2"
  ;!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  !insertmacro MUI_PAGE_STARTMENU Application $STARTMENU_FOLDER

  !insertmacro MUI_PAGE_INSTFILES
  !define MUI_FINISHPAGE_RUN "$INSTDIR\metamorphose2.exe"
  !insertmacro MUI_PAGE_FINISH

  ;uninstall
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_COMPONENTS
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections


; win2000 needs GdiPlus.dll
Function win2000
  ReadRegStr $R0 HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion
  StrCmp $R0 "5.0" lbl_done

  lbl_done:

FunctionEnd

Section "Métamorphose2" Application

  SectionIn RO
  SetOutPath "$INSTDIR"

  File /r _win_bin\*
  File gdiplus.dll
  File msvcp71.dll
  
  ;Install for all users
  SetShellVarContext all

  Call win2000

  ;Store installation folder
  WriteRegStr HKLM "Software\metamorphose2" "" $INSTDIR
  WriteRegStr HKLM "Software\metamorphose2" "version" ${VERSION}

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    ;Create shortcuts
    CreateDirectory "$SMPROGRAMS\$STARTMENU_FOLDER"
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Métamorphose2.lnk" "$INSTDIR\metamorphose2.exe"
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

Section "Right-click menu" Shell
  WriteRegStr HKCR "Directory\shell\Rename with Métamorphose2" "" ""
  WriteRegStr HKCR "Directory\shell\Rename with Métamorphose2\command" "" "$INSTDIR\metamorphose2.exe %L"
SectionEnd

Section "Desktop Shortcut" DShortCut
  CreateShortCut "$DESKTOP\Métamorphose2.lnk" "$INSTDIR\metamorphose2.exe"
SectionEnd

Section /o "Quicklaunch Shortcut" QShortCut
  CreateShortCut "$QUICKLAUNCH\Métamorphose2.lnk" "$INSTDIR\metamorphose2.exe"
SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_Application ${LANG_ENGLISH} "The main application files (required)."
  LangString DESC_Shell ${LANG_ENGLISH} "Add this right-click menu option: 'Rename with Métamorphose2'."
  LangString DESC_DShortCut ${LANG_ENGLISH} "Create a Desktop shortcut."
  LangString DESC_QShortCut ${LANG_ENGLISH} "Create a Quickstart shortcut."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${Application} $(DESC_Application)
    !insertmacro MUI_DESCRIPTION_TEXT ${Shell} $(DESC_Shell)
    !insertmacro MUI_DESCRIPTION_TEXT ${DShortCut} $(DESC_DShortCut)
    !insertmacro MUI_DESCRIPTION_TEXT ${QShortCut} $(DESC_QShortCut)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END


;--------------------------------
;Uninstaller Section

Section "un.Métamorphose" Uninstall

  SectionIn RO
  
  ;Uninstall for all users
  SetShellVarContext all

  Delete "$DESKTOP\Métamorphose2.lnk"
  Delete "$QUICKLAUNCH\Métamorphose2.lnk"

  !insertmacro MUI_STARTMENU_GETFOLDER Application $MUI_TEMP
  RMDir /r "$SMPROGRAMS\$MUI_TEMP"

  RMDir /r "$INSTDIR"

  ;DeleteRegKey HKCU "Software\metamorphose2"
  DeleteRegKey HKLM "Software\metamorphose2"
  DeleteRegKey HKCR "Directory\shell\Rename with Métamorphose2"
  DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\metamorphose2"

SectionEnd

Section /o "un.User files" UninstallUser
  
  ;remove config for current user
  SetShellVarContext current
  
  RMDir /r "$APPDATA\.metamorphose2"

SectionEnd

  ;Language strings
  LangString DESC_Uninstall ${LANG_ENGLISH} "The main application files (required)."
  LangString DESC_UninstallUser ${LANG_ENGLISH} "Current user's configuration and history files."

  ;Assign language strings to sections
  !insertmacro MUI_UNFUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${Uninstall} $(DESC_Uninstall)
    !insertmacro MUI_DESCRIPTION_TEXT ${UninstallUser} $(DESC_UninstallUser)
  !insertmacro MUI_UNFUNCTION_DESCRIPTION_END
