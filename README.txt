This is a utility that is meant to replace the default rm command in BASH. It moves
files to a folder (~/.trash) instead of deleting them. Thus, you can undelete files
easily with the command
    `rm -u`.
The program shouldn't be slower than actual deletion, and the trash can be emptied when
it fills up, with
    `rm -e`.

The trash folder is initialized in ~/.trash, with the logfile ~/.trash/TRASH_LOG.log.
This can easily be changed by editing the TRASH variable in the source.

