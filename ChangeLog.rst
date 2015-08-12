***********************
Métamorphose2 Changelog
***********************

2.0.8.4 beta
============
**2015-08-11**

Source only release. Will a real packager please stand up?

Fixes/Changes:
  - Improved cross OS/shell compatibility — Javier Prats
  - Improved FreeBSD compatibility — Javier Prats
  - Properly import the Image module from PIL(low) — ShadowKyogre
  - Update to mutagen 1.28
  - Update to exif-py 2.1.1
  - Whitespace & except improvements
  - Enlarge width of operations list
  - Style/PEP8 improvements
  - Move option parsing to earlier in the startup process

Additions:
  - Allow setting the wxPython version in CLI options
  - rST readme and changelog


2.0.8.3 beta
============
**2011-??-??**

Fixes/Changes:
  - Upgrade to latest version of mutagen, 1.20
  - Bug fix, m4a extension now correctly identified as audio file.
  - Change "Destroy" to "Delete" for operations (ticket 146403).

Additions:
  - Allow recursive folder renaming (finally!)
  - Get audio metadata from m4a/mp4 files.


2.0.8.2 beta
============
**2011-01-07**

Fixes/Changes:
  - Fix bug folder periods (ticket 3148632).
  - Continue better centralized variable storage.
  - Change color picker buttons.
  - Minor bugfixes.
  - Translation updates.

Additions:
  - Allow recursive folder renaming in debug mode (!)


2.0.8.1 beta
============
**2010-12-31**

Fixes/Changes:
  - Fix bug with duplicate rename (ticket 3095633).
  - Fix bug with config file load/save (ticket 3148071).
  - Fix bug with removing items from error panel.
  - Preferences dialog now uses toolbar.
  - Start using better centralized variable storage.
  - Minor bugfixes.
  - Translation updates.


2.0.8.0 beta
============
**2010-12-16**

Fixes/Changes:
  - Miscellaneous minor bug fixes.
  - Track numbers are now auto-padded with 0 when needed.
  - Speed and memory usage improvements to error panel.
  - Configs folder now defaults to user home (ticket 2803288).
  - Home folder in Windows no longer has leading period.
  - MAJOR rewrite of method names and code documentation, this makes
      contributing to Métamorphose2 much easier and more pleasant than before.
  - Begin setting some methods to 'private' for clearer view of modularity.

Additions:
  - Allow changing highlight colors (ticket 2783757)
  - Copy file name in directory (ticket 3019859).
  - Save list of errors to file.
  - 'Reset' menu item to clear all settings.


2.0.7.1 beta
============
**2010-06-20**

Fixes/Changes:
  - Fix preferences not opening (ticket 2995714).
  - Fix issue with wrong encoder when loading items from directory.
  - Improvements to French translation.
  - Many miscellaneous fixes & code cleanup.

Additions:
  - Organize operations by drag & drop.
  - Start converting to python 3.
  - Use system fonts under GTK


2.0.7.0 beta
============
**2010-03-26**

Fixes/Changes:
  - Fix multiple preference problems by changing how settings are accessed.
  - Fix inconsistent highlighting (ticket 2974367).
  - Fix Ubuntu/Debian install issue with .desktop file (ticket 2967145).

Additions:
  - Preliminary Spanish Translation.


2.0.6.6 beta
============
**2010-03-02**

Fixes/Changes:
  - Fixed some command line options bugs.
  - Fixed dialog crash (ticket 2948461).
  - Fixed admin privileges bug in Windows Vista / 7.

Additions:
  - Command line options to manpage.


2.0.6.5 beta
============
**2009-10-14**

Fixes/Changes:
  - Installer problems in multi-user winXP systems (ticket 2868067).
  - Some crashes on renaming (import wx error).
  - Refresh during rename works again.
  - Loading a config with no path set does not override the path.

Additions:
  - Renamer menu.
  - Some internal changes for better modularity.


2.0.6.4 beta
============
**2009-09-14**

Fixes/Changes:
  - Fixed XML encoding error in config files (ticket 2859515).
  - Fixed 'apply to' checkboxes not saving in config files (ticket 2803294).

Additions:
  - Some internal changes for better modularity.


2.0.6.3 beta
============
**2009-08-30**

Fixes/Changes:
  - Some fixes related to the mutagen library integration.
  - Some minor clarifications to program wording.
  - Continuing source code reorganization.

Additions:
  - Improvements to manual edit dialog as requested in ticket # 2803281.


2.0.6.2 beta
============
**2009-08-15**

Fixes/Changes:
  - Now using ``Mutagen`` for all audio metadata retrieval.
  - Fix bug 2837523 : "FilterSel" Field remains empty in config file.

Additions:
  - Mutagen allows getting metadata from almost all types of audio files, not
      just mp3 as before.


2.0.6.1 beta
============
**2009-08-03**

Fixes/Changes:
  - Fix manual edit not error checking bug (id# 2794757)
  - Fix operation numbering bug (ticket 2794751) — Kenneth Murphy
  - More modularizing of internal components
  - Fix config extension not shown by default in linux bug (ticket 2803293)

Additions:
  - Allow copying from a read-only location.
  - More options for removing files in preview list
  - Only show changed items option (id# 2831192)


2.0.6.0 beta
============
**2009-02-28**

Fixes/Changes:
  - Major re-arrange of source file structure for more logical layout.
  - Major work on modularizing internal components. This will allow many future improvements and features.
  - Code style updates.
  - Removal/merging of redundant code.
  - Some minor speed improvements.

Additions:
  - Recursive renaming of folders. (Highly experimental, only active in debug mode)
  - Command line option : set auto mode level
  - More debug and time outputs.


2.0.5.0 beta
============
**2008-10-29**

Fixes/Changes:
  - Config file issues.
  - Exif tag processing bugs.
  - Id3 tag retrieval.
  - Allow setting directory placement when sorting by stat.
  - Missing dll files in Windows Installer.
  - Preference issues under Windows.

Additions:
  - Command line options processing.
  - Command line options : show options, debug mode, timer mode, load config file, set language


2.0.4.3 beta
============
**2008-06-15**

Fixes/Changes:
  - Sizing and layout issues.
  - Freeze on some Exif files (patch by James Marjie).

Additions:
  - Command line options.
  - French translation.
  - Sort on item attributes.
  - Recursive depth option.
  - Manual editing of names.
  - Progress dialog when previewing many items.
  - Progress dialog preferences.
  - File extension related picker filters.
  - Dupe numbering (experimental).


2.0.4.2 beta
============
**2008-04-01**

Fixes/Changes:
  - Date formatting problem for config file on some non-English systems.
  - String conversion bug in error panel.
  - Bug when deselecting twice from error panel.

Additions:
  - wxPython version checking: require 2.6, prefer 2.8.


2.0.4.1 beta
============
**2008-03-05**

Fixes/Changes:
  - Some annoying error pop ups redirected to standard error instead.
  - Much faster loading of Exif data.
  - Images now re-preview only when the thumbnail size is changed.
  - Update accent strip.
  - Uninstaller now removes quick-launch links.

Additions:
  - *Finally* — Full saving and loading of configuration files!
      All operation parameters can be saved to configuration files, all settings can be loaded.
  - Preferences: change renaming refresh rate
  - Preferences: split 'automation' and 'logging' panels.
  - Windows binary compiled under python 2.5.2, wxPython 2.8.7.1
  - Installer adds GdiPlus.dll for Windows 2000.


2.0.3.2 beta
============
**2007-12-21**

Fixes/Changes:
  - Lots of code cleanup and various fixes.
  - Preview speed increased.
  - Renaming speed increased.
  - Selection list (picker) is now much faster for multiple selections.
  - Preview now uses less memory.
  - Rewrite of config file functions to use XML.
  - Renaming across filesystems.
  - Date/Time from EXIF.
  - Double loading bug.
  - Directory operations bugs in Windows.
  - Loading directory bug in Windows.
  - Images not found when loading application bug.
  - Improper command line path parsing.

Additions:
  - Show which files will be modified.
  - Modifications: encoding conversions.
  - Preferences: show thumbnails in preview, highlight changed files.
  - Expanded operations right click menu.
  - Config file saves operation type and order.
  - Date/time from EXIF: original, modified.
  - Windows installer.


2.0.2.1 beta
============
**2007-09-04**

Fixes/Changes:
  - Lots of code cleanup and various small fixes.
  - Makefile — Pierre-Yves Chibon
  - Some sizing issues.
  - Rewrite of positions.
  - Some issues with RE functions.
  - Issues with directory operation.
  - Names of operations (a bit more understandable now)

Additions:
  - Drag and Drop operations.
  - Right-click menu for operations.
  - Modifications: strip accents (cnvert to ASCII), url-decode, 1337.
  - Removed buttons for id3 and exif, access functions by choice list now.
  - Sort by specific position.
  - Options for logging — separator, encloser, file extension.
  - 256px sized preview, removed 16px.
  - Nicer text in intro panel.


2.0.2.0 beta
============
**2007-07-13**

*First beta version wOOt!*

Fixes/Changes:
  - Lots of code cleanup and various small fixes.
  - Repetitive functions go to separate utils file.
  - Redo of preferences for easier maintenance.
  - Preferences now correctly identifies version (again!).

Additions:
  - Project to SVN repository.
  - Image preview in various sizes in picker and preview as requested by Joerg Desch.
  - Undo button in main windows as requested by Joerg Desch.
  - Show item type (file, folder) in preview.
  - Lots of new icons, from the Fedora project.
  - Saving and loading of a *basic* configuration file.
  - Loading selection from CSV file.


2.0.1.7 alpha
=============
**2007-05-15**

Fixes/Changes:
  - Several problems as reported by William Swearingen.
  - Some fixes for directory path structure checking.
  - Preferences now correctly identifies version.

Additions:
  - Save as CSV now works.
  - Removal of items with errors/warnings now possible.


2.0.1.6 alpha
=============
**2007-04-24**

Fixes/Changes:
  - More sizing issues, various platforms.
  - Fixed crash on radio button change under win2000.
  - On language initialization error, popup message suppressed.

Additions:
  - Swap now works for single character matches.
  - More sorting options for directories.
  - Directory path structure checking, functional but not complete.
  - Regular expression quick buttons.
  - Changes to how modules are handled for easier plugins.
  - Add parent folder name into file/folder name, per requests.
  - When filename exists suggest using sub-folder for renaming.


2.0.1.5 alpha
=============
**2007-04-03**

Fixes/Changes:
  - Icon not displaying errors.
  - More sizing issues, various platforms.
  - Bug that caused lost files under UNIX filesystems.
  - Regular expressions problems.

Additions:
  - 'Destroy all operations' button.
  - 'Reset current operation' button.
  - Insert in between text finished.


2.0.1.4 alpha
=============
**2007-03-24**

Fixes/Changes:
  - Lots of small fixes and adjustments.

Additions:
  - Swap operation (only GUI as of now)
  - Insert in between text (not functional yet).
  - Rewrite of regular expressions for more uniform look (almost done).
  - The main interface is now split horizontally, allows resizing.


2.0.1.3 alpha
=============
**2007-03-05**

Fixes/Changes:
  - Some sizing issues.
  - Various bugs that crashed the program.
  - Various less serious bugs.
  - Alpha padding issues.

Additions:
  - Match in between text in search.
  - Insert in between text (not functional yet).
  - Repeating the same number when counting.
  - Regular expression quick buttons.


2.0.1.2 alpha
=============
**2007-02-14**

Fixes/Changes:
  - Numbering auto pad when counting down.
  - text boxes trigger preview on text change.

Additions:
  - Intelligent sorting of unpadded numbers.
  - Better language support (for later).
  - All Métamorphose1 counting parameters!
  - Numbering sequences are now unique for each operation.


2.0.1.1 alpha
=============
**2007-02-09**

Fixes/Changes:
  - Regular expression for replace operation.

Additions:
  - Regular expression error messages.
  - Better handling of warnings/errors.
  - Option to sort directories first.
  - Some new icons from http://www.deviantart.com/deviation/37966044
