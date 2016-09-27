from __future__ import unicode_literals, absolute_import, print_function

import os
posixpath


class SlideshowMixin(object):
    def get_slideshow(self, slideshow_id=None, slideshow_url=None, **optional):
        """Get slideshow information by id or url

        Args:
            slideshow_id (int):
                id of the slideshow to be fetched. Precedence over slideshow_url.
            slideshow_url (string):
                URL of the slideshow to be fetched.
                Optional if `slideshow_id` specified
            username (string):
                username of the requesting user [Optional]
            password (string):
                password of the requesting user [Optional]
            exclude_tags (boolean):
                Exclude tags from the detailed information. 1 to exclude. [Optional]
            detailed (boolean):
                Set to 1 to include optional information (tags, for example)
                Defaults to None. If None only basic information attached [Optional]
            get_transcript (boolean):
                Set it to 1 if you want to return with transcript parameter
                in the response. requires detailed to be set to 1. [Optional]

        """
        params = {}
        params = self.prefetch_default_credentials(params, optional)
        if slideshow_id:
            params["slideshow_id"] = slideshow_id
        elif slideshow_url:
            params["slideshow_url"] = slideshow_url
        else:
            raise ValueError("get_slideshow: slideshow_id or "
                             "slideshow_url must be specified")

        if "exclude_tags" in optional:
            params["exclude_tags"] = int(bool(optional["exclude_tags"]))

        if "detailed" in optional:
            params["detailed"] = int(bool(optional["detailed"]))

        if "get_transcript" in optional:
            params["get_transcript"] = int(bool(optional["get_transcript"]))

        params.update(self.params)
        return self.get('get_slideshow', **params)

    def get_slideshows_by_tag(self, tag, **optional):
        """ Get slideshows by tag

        Args:
            tag (string):
                tag name
            limit (int):
                specify number of items to return. Default to 10. [Optional]
            offset (int):
                specify offset [Optional]
            detailed (boolean):
                Set to 1 to include optional information (tags, for example)
                Defaults to None. If None only basic information attached [Optional]

        """
        params = {"tag": tag}

        if "limit" in optional:
            try:
                params["limit"] = int(optional.get("limit"))
            except ValueError:
                raise ValueError("get_slideshows_by_tag: invalid "
                                 "value for {}".format(optional.get("limit")))
        else:
            params["limit"] = 10

        if "offset" in optional:
            try:
                params["offset"] = int(optional.get("offset"))
            except ValueError:
                raise ValueError("get_slideshows_by_tag: invalid "
                                 "value for {}".format(optional.get("offset")))

        if "detailed" in optional:
            params["detailed"] = int(bool(optional["detailed"]))

        return self.get('get_slideshows_by_tag', **params)

    def edit_slideshow(self, slideshow_id, **optional):
        """Edit existing slideshow

        Args:
            slideshow_id (int):
                Id of slideshow which is being deleted
            username (string):
                Owner username of the slideshow which is being edited
            password (string):
                Owner password of the slideshow which is being edited
            slideshow_title (string):
                Title of the slideshow.
            slideshow_description (string):
                Slideshow description
            slideshow_tags (string or list):
                Comma separated list of tags
            make_slideshow_private (enumerated):
                Should be Y if you want to make the slideshow private. If this
                is not set, following tags will not be considered. [Optional]
            generate_secret_url (enumerated):
                Generate a secret URL for the slideshow.
                Requires make_slideshow_private to be Y. [Optional]
            allow_embeds (enumerated):
                Sets if other websites should be allowed to embed the slideshow.
                Requires make_slideshow_private to be Y. [Optional]
            share_with_contacts (enumerated):
                Sets if your contacts on SlideShare can view the slideshow.
                Requires make_slideshow_private to be Y. [Optional]

        Returns:
            xml: XML with slideshare ID if success.

            Example:
                .. code-block:: xml

                    <SlideShowEdited>
                      <SlideShowID>SlideShowID</SlideShowID>
                    </SlideShowEdited>

        """
        params = {}
        params = self.prefetch_default_credentials(params, optional,
                                                   required=True)
        params["slideshow_id"] = int(slideshow_id)

        if "slideshow_title" in optional:
            params["slideshow_title"] = optional["slideshow_title"]
        if "slideshow_description" in optional:
            params["slideshow_description"] = optional["slideshow_description"]

        if "slideshow_tags" in optional:
            if isinstance(optional["slideshow_tags"], list):
                params["slideshow_tags"] = ",".join(
                    optional.get("slideshow_tags"))
            else:
                params["slideshow_tags"] = optional.get("slideshow_tags")

        if optional.get("make_src_public", "Y") == "N":
            params["make_src_public"] = "N"

        if optional.get("make_slideshow_private", "N") == "Y":
            params["make_slideshow_private"] = "Y"

        if optional.get("generate_secret_url", "N") == "Y":
            if "make_slideshow_private" not in params:
                raise ValueError("upload_slideshow: make_slideshow_private must"
                                 " be set to Y if you want generate secret url")
            params["generate_secret_url"] = "Y"

        if optional.get("allow_embeds", "N") == "Y":
            if "make_slideshow_private" not in params:
                raise ValueError("upload_slideshow: make_slideshow_private must"
                                 " be set to Y if you want allow embeds")
            params["allow_embeds"] = "Y"

        return self.get('edit_slideshow', **params)

    def delete_slideshow(self, slideshow_id, **optional):
        """Deletes a slideshow

        Args:
            slideshow_id (int):
                Id of slideshow which is being deleted
            username (string):
                Owner username of the slideshow which is being deleted
            password (string):
                Owner password of the slideshow which is being deleted

        """
        params = {}
        params = self.prefetch_default_credentials(params, optional,
                                                   required=True)
        params["slideshow_id"] = int(slideshow_id)

        return self.get('delete_slideshow', **params)

    def upload_slideshow(self, slideshow_title, slideshow_srcfile=None,
                         upload_url=None, **optional):
        """ Upload slideshow.

        Sent POST-request if `slideshow_srcfile` provided, otherwise send GET.
        The document will upload into the account of the user specified
        by (username / password).
        The user associated with the API key need not be the same as the
        user into who's account the slideshow gets uploaded. So, for example,
        a bulk uploader would include the api_key (and hash) associated with
        the API account, and the username and password associated with the
        account being uploaded to.

        Note:
            This method requires extra permissions. If you want to upload
            a file using SlideShare API, please send an email to
            api@slideshare.com with your developer account username
            describing the use case.

        Args:
            slideshow_title (string):
                Title of the slideshow.
            username (string):
                username of the requesting user.
                Optional if default provided. [Optional]
            password (string):
                password of the requesting user.
                Optional if default provided. [Optional]
            slideshow_srcfile (string):
                Slideshow file path. Precedence over upload_url.
            upload_url (string):
                String containing an url pointing to the power point file. Example::

                    http://domain.tld/directory/my_power_point.ppt

                The following urls are also acceptable::

                    http://www.domain.tld/directory/file.ppt
                    http://www.domain.tld/directory/file.cgi?filename=file.ppt

                Note:
                    This will not accept entries that cannot be identified
                    by their extension. Example::

                        http://www.domain.tld/directory/file.cgi?id=2342

                Optional if slideshow_srcfile provided.
            slideshow_description (string):
                Slideshow description
            slideshow_tags (string or list):
                Comma separated list of tags
            make_src_public (enumerated):
                Y if you want users to be able to download the ppt file,
                N otherwise. Default is Y [Optional]
            make_slideshow_private (enumerated):
                Should be Y if you want to make the slideshow private. If this
                is not set, following tags will not be considered. [Optional]
            generate_secret_url (enumerated):
                Generate a secret URL for the slideshow.
                Requires make_slideshow_private to be Y. [Optional]
            allow_embeds (enumerated):
                Sets if other websites should be allowed to embed the slideshow.
                Requires make_slideshow_private to be Y. [Optional]
            share_with_contacts (enumerated):
                Sets if your contacts on SlideShare can view the slideshow.
                Requires make_slideshow_private to be Y. [Optional]

        Returns:
            xml: XML with slideshare ID if success.

            Example:
                .. code-block:: xml

                    <SlideShowUploaded>
                        <SlideShowID>{slideshow id goes here}</SlideShowID>
                    </SlideShowUploaded>

            Slideshow id will be necessary for retrieving the slideshow
            embed code, once the slideshow has been converted into flash.

        """
        params = {}
        params = self.prefetch_default_credentials(params, optional)
        params["slideshow_title"] = slideshow_title
        upload_file = {}
        if slideshow_srcfile:
            # Workaround to deal with filenames containing non-ASCII symbols.
            _, ext = posixpath.splitext(slideshow_srcfile)
            valid_fname = 'slideshow_srcfile' + ext
            upload_file = [
                (valid_fname, (valid_fname, open(slideshow_srcfile, 'rb')))]
        elif upload_url:
            params["upload_url"] = upload_url
        else:
            raise ValueError("upload_slideshow: slideshow_srcfile or "
                             "upload_url must be provided")
        params["slideshow_description"] = optional.get("slideshow_description",
                                                       "")
        if "slideshow_tags" in optional:
            if isinstance(optional["slideshow_tags"], list):
                params["slideshow_tags"] = ",".join(
                    optional.get("slideshow_tags"))
            else:
                params["slideshow_tags"] = optional.get("slideshow_tags")

        if optional.get("make_src_public", "Y") == "N":
            params["make_src_public"] = "N"

        if optional.get("make_slideshow_private", "N") == "Y":
            params["make_slideshow_private"] = "Y"

        if optional.get("generate_secret_url", "N") == "Y":
            if "make_slideshow_private" not in params:
                raise ValueError("upload_slideshow: make_slideshow_private must"
                                 " be set to Y if you want generate secret url")
            params["generate_secret_url"] = "Y"

        if optional.get("allow_embeds", "N") == "Y":
            if "make_slideshow_private" not in params:
                raise ValueError("upload_slideshow: make_slideshow_private must"
                                 " be set to Y if you want allow embeds")
            params["allow_embeds"] = "Y"

        if optional.get("share_with_contacts", "N") == "Y":
            if "make_slideshow_private" not in params:
                raise ValueError("upload_slideshow: make_slideshow_private must"
                                 " be set to Y if you want allow to share"
                                 "slideshow with contacts")
            params["share_with_contacts"] = "Y"

        if slideshow_srcfile:
            return self.post('upload_slideshow', files=upload_file, data=params)
        else:
            return self.get('upload_slideshow', **params)

