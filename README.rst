=========
mediamosa
=========

mediamosa is a python wrapper for accessing a mediamosa api.

------------
Installation
------------

Install mediamosa as follows:

::

   pip install mediamosa

-----
Usage
-----

::

    >>> from mediamosa.api import MediaMosaAPI
    >>> api = MediaMosaAPI('http://apivideo.ugent.be')
    >>> api.authenticate('USERNAME', 'PASSWORD')
    True
    >>> api.asset_list()
    [<mediamosa.resources.Asset GAKkgcmMPaIZdMl3dczqUESA>, <mediamosa.resources.Asset KWdqPljZge6ESLWbPdEEcG0j>, <mediamosa.resources.Asset d1bbGsmEjXmeSfM8PGT5uRjB>, <mediamosa.resources.Asset uKgRwHGTidLLiTiSUQu26buN>, <mediamosa.resources.Asset x2XRGwefXfNvoRNYLJjfWS5O>, <mediamosa.resources.Asset ONZDQiGfhTf8OcsKumKISpOy>, <mediamosa.resources.Asset A1lkCZclpXaWSLE9RPK4Pthk>, <mediamosa.resources.Asset A2TmfbWMcMU6r8jWHOS2JEsf>, <mediamosa.resources.Asset B7zsZXLvnnLCCIyJOrCQxxRl>, <mediamosa.resources.Asset C2VNSEfaeMc7ToOeirEqiztz>]
    >>> list = api.asset_list()
    >>> len(list)
    84
