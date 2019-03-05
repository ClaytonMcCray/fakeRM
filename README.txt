This is a utility that is meant to replace the default rm command in BASH. It moves
files to a folder (~/.trash) instead of deleting them. Thus, you can undelete files
easily with the command
    `rm -u`.
The program shouldn't be slower than actual deletion, and the trash can be emptied when
it fills up, with
    `rm -e`.

The trash folder is initialized in ~/.trash, with the logfile ~/.trash/TRASH_LOG.log.
This can easily be changed by editing the TRASH variable in the source.

-------------------------------------------------------
Usage:
    Detailed options can be seen with
        rm -h
    But, standard usage is
        rm FILE1 FILE2 ...
    to delete regular files, and
        rm -r DIR1 DIR2 ...
    to delete directories.

    The trash can be cleaned out with
        rm -e
    and the most recently deleted file can be undeleted to the original location with
        rm -u
    After this file is restored, the next file can be undeleted.

