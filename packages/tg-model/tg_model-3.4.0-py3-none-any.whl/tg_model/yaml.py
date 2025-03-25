# -*- coding: utf-8 -*-
# Copyright (C) 2023-2025 TUD | ZIH
# ralf.klammer@tu-dresden.de

import logging

from copy import deepcopy

from yaml import full_load as load_yaml  # type: ignore
from pkgutil import get_data
from os import listdir, path
from pyaml import dump as dump_yaml  # type: ignore


from .other_files import OtherFiles
from .util import (
    split_xpath,
    exists,
    find_name_of_subproject,
    prepare_path,
    get_files,
    deref_multi,
    find_tei_directory,
    strip_strings_in_dict,
    extract_unique_name,
)

log = logging.getLogger(__name__)


class CollectionMixin(object):

    @property
    def collection(self):
        return self.content["collection"]

    @property
    def elements(self):
        return self.collection["elements"]

    @property
    def sorted_elements(self):
        return sorted(self.elements, key=lambda x: (x["filename"]))

    @property
    def title(self):
        return self.collection["title"]

    def short_title(self, value=None):
        if value:
            self.title["short"] = value
        return self.title["short"]

    def long_title(self, value=None):
        if value:
            self.title["long"] = value
        return self.title["long"]

    def _get_or_set_multi_item(self, key, value=None):
        if value:
            self.collection[key] = value
        return (
            self.collection[key]
            if key in self.collection
            and isinstance(self.collection[key], list)
            else []
        )

    def basic_classifications(self, value=None):
        return self._get_or_set_multi_item("basic_classifications", value)

    def rights_holder(self, value=None):
        return self._get_or_set_multi_item("rights_holder", value)

    def collector(self, value=None):
        return self._get_or_set_multi_item("collector", value)

    def gnd_subjects(self, value=None):
        return self._get_or_set_multi_item("gnd_subjects", value)


class YAMLConfigBase(object):
    def __init__(
        self, filename, projectpath=None, subproject=None, *args, **kw
    ):
        self.filename = filename
        self.projectpath = projectpath
        self.subproject = subproject
        if subproject:
            self.path = "%s/%s" % (subproject["basepath"], filename)
        else:
            self.path = "%s/%s" % (projectpath, filename)
        self._content = False

    @property
    def content(self):
        if self._content is False:
            self._content = None
            _data = self.get_data()
            if _data:
                self._content = load_yaml(_data)
        return self._content

    def get_data(self):
        if exists(self.path):
            with open(self.path, "rb") as file:
                return file.read()
        else:
            log.error("%s does not exist!" % self.path)

    def _get(self, key, _dict=None):
        _dict = self.content if _dict is None else _dict
        if key not in _dict:
            return None
        else:
            value = _dict[key]
            log.debug("[_get] value: %s | key: %s" % (value, key))
            return value if value else {}

    def get(self, key, section=None, default=None):
        section_name = section
        section = None
        if section_name:
            section = self._get(section_name)
            if section is None:
                log.error(
                    "Section_name: '%s' not found in %s"
                    % (section_name, self.path)
                )
        value = self._get(key, _dict=section)
        if value:
            return value
        else:
            log.info(
                "'%s' not found in section_name: %s (%s)"
                % (key, section_name, self.path)
            )
            return default

    def exists(self):
        log.debug("This check for existance is very rough!!!")
        return bool(self.content)


class MainConfig(YAMLConfigBase):
    def __init__(self, *args, **kw):
        super().__init__("main.yaml", *args, **kw)
        self.other_files = OtherFiles(self.projectpath, self)

    def validate(self):
        request = []
        # check if there are any files in the given inputpath
        for subproject in self.content["subprojects"]:
            if not get_files(subproject["inpath"]):
                request.append(
                    "No XML files found at: %s" % subproject["inpath"]
                )
        return request

    def _check_files(self):
        save = False
        for subproject in self.content["subprojects"]:
            if "files" not in subproject:
                subproject["files"] = sorted(get_files(subproject["inpath"]))
                save = True
        if save:
            self.save()

    def get_subprojects(self):
        if self.exists():
            self._check_files()
            return deepcopy(self.content["subprojects"])
        else:
            return []

    def get_subproject(self, name=None, inpath=None):
        for sp in self.get_subprojects():
            if name and sp["name"] == name:
                return sp
            if inpath and sp["inpath"] == inpath:
                return sp
        return None

    @property
    def min_hitrate(self):
        return self.get("min_hitrate", section="proposals", default=50)

    def set_subproject_stats(self):
        for subproject in self.get_subprojects():
            files = [
                f
                for f in listdir(subproject["inpath"])
                if not path.isdir("%s/%s" % (subproject["inpath"], f))
            ]
            subproject["stats"] = {"files": len(files)}

    def save(self):
        with open(self.path, "w") as file:
            file.write(dump_yaml(self.content))

    def update(
        self,
        inputpath=None,
        sourcepath=None,
        tei_directory=None,
        tei_directories=None,
        **kw,
    ):
        if sourcepath and tei_directory:
            tei_directories = find_tei_directory(sourcepath, tei_directory, 0)
        elif inputpath:
            tei_directories = inputpath.split(",")
        elif tei_directories is not None:
            pass
        else:
            log.error("Neither 'sourcepath' nor 'inputpath' is defined!")
            raise ValueError

        log.debug("tei_directories: %s" % tei_directories)
        existing_subprojects = []
        for sp in self.get_subprojects():
            if sp["inpath"] in tei_directories:
                existing_subprojects.append(sp["name"])
            else:
                # shutil.rmtree(sp["basepath"])
                self.content["subprojects"].remove(sp)

        # ToDo: merge the following code with the same code in
        # MainConfigTemplate.render
        for p in tei_directories:
            prepared_path = prepare_path(p)
            splitted_pp = prepared_path.split("/")
            length = 3 if len(splitted_pp) >= 3 else len(splitted_pp)

            if sourcepath:
                # try to find name of subproject only if there is more
                # than one subproject
                if len(tei_directories) > 1:
                    input_name = find_name_of_subproject(
                        kw["projectname"], p, tei_directory
                    )
                if len(tei_directories) <= 1 or not input_name:
                    input_name = sourcepath.split("/")[-1]
            else:
                input_name = "_".join(splitted_pp[-length:])

            if input_name in existing_subprojects:
                continue

            outpath = prepare_path(
                (
                    kw["outputpath"]
                    if "outputpath" in kw and kw["outputpath"]
                    else self.projectpath
                ),
                subpath="/".join([input_name, "result"]),
                create=True,
            )

            basepath = prepare_path(
                self.projectpath,
                subpath=input_name,
                create=True,
            )

            self.content["subprojects"].append(
                {
                    "inpath": prepared_path,
                    "name": input_name,
                    "outpath": outpath,
                    "basepath": basepath,
                    "files": sorted(get_files(prepared_path)),
                }
            )

        self.other_files.init(self.content["project"])
        self.save()


class CollectionConfig(YAMLConfigBase, CollectionMixin):
    def __init__(self, *args, **kw):
        super().__init__("collection.yaml", *args, **kw)
        self._attributes = None
        self._work = None
        self._edition = None
        self._eltec_specs = None
        self._as_dict = None

    def save(self):
        if not self.filename:
            raise Exception("No filename given for YAMLConfigTemplate!")
        with open(self.path, "w") as file:
            file.write(dump_yaml(self.content))

    @property
    def attributes(self):
        if self._attributes is None:
            self._attributes = self.content["collection"]["attributes"]
        return self._attributes

    @property
    def work(self):
        if self._work is None:
            self._work = self.attributes["work"]
        return self._work

    @property
    def edition(self):
        if self._edition is None:
            self._edition = self.attributes["edition"]
        return self._edition

    @property
    def eltec_specs(self):
        if self._eltec_specs is None:
            self._eltec_specs = self.content["collection"]["eltec_specs"]
        return self._eltec_specs

    def get_missing_params(self):
        missing_params = []
        for k in ["short", "long"]:
            keys = ["collection", "title", k]
            if deref_multi(self.content, keys) is None:
                missing_params.append(".".join(keys))
        return missing_params

    def get_dict(self):
        if self._as_dict is None:
            self._as_dict = strip_strings_in_dict(self.content["collection"])
        return self._as_dict


class YAMLConfigTemplate(YAMLConfigBase):
    def __init__(self, filename, projectpath, subpath=None, *args, **kw):
        self.projectpath = prepare_path(projectpath, create=True)

        super().__init__(filename, self.projectpath, *args, **kw)

    def get_data(self):
        return get_data(__name__, "templates/%s" % self.filename)

    def save(self):
        if not self.filename:
            raise Exception("No filename given for YAMLConfigTemplate!")
        with open(self.path, "w") as file:
            file.write(dump_yaml(self.content, sort_keys=False))


class MainConfigTemplate(YAMLConfigTemplate):
    def __init__(self, *args, **kw):
        super().__init__("main.yaml", *args, **kw)

    def render(
        self,
        inputpath=None,
        tei_directories=None,
        sourcepath=None,
        tei_directory=None,
        **kw,
    ):
        if sourcepath and tei_directory:
            tei_directories = find_tei_directory(sourcepath, tei_directory, 0)
        elif inputpath:
            tei_directories = inputpath.split(",")
        elif tei_directories:
            pass
        else:
            log.error("Neither 'sourcepath' nor 'inputpath' is defined!")
            raise ValueError

        log.debug("tei_directories: %s" % tei_directories)

        # ToDo: merge the following code with the same code in
        # MainConfig.update
        subprojects = []
        unique_names = extract_unique_name(tei_directories)
        for p in tei_directories:
            prepared_path = prepare_path(p)
            splitted_pp = prepared_path.split("/")
            length = 3 if len(splitted_pp) >= 3 else len(splitted_pp)

            # Try to get a unique name for the subproject
            # 1. check if the name is in the list of unique names
            input_name = None
            for unique_name in unique_names:
                if unique_name in p:
                    input_name = unique_name
                    break
            # 2. if not, try to find a name in the path
            if not input_name:
                # 2.1 if sourcepath is given try to find name of subproject
                # only if there is more than one subproject
                if sourcepath:
                    if len(tei_directories) > 1:
                        input_name = find_name_of_subproject(
                            kw["projectname"], p, tei_directory
                        )
                    if len(tei_directories) <= 1 or not input_name:
                        input_name = sourcepath.split("/")[-1]
                # 2.2 if sourcepath is not given, use the last parts of path
                else:
                    input_name = "_".join(splitted_pp[-length:])

            outpath = prepare_path(
                (
                    kw["outputpath"]
                    if "outputpath" in kw and kw["outputpath"]
                    else self.projectpath
                ),
                subpath="/".join([input_name, "result"]),
                create=True,
            )

            basepath = prepare_path(
                self.projectpath,
                subpath=input_name,
                create=True,
            )

            subprojects.append(
                {
                    "inpath": prepared_path,
                    "name": input_name,
                    "outpath": outpath,
                    "basepath": basepath,
                    "files": sorted(get_files(prepared_path)),
                }
            )

        self.content["subprojects"] = subprojects

        OtherFiles(self.projectpath, None).init(self.content["project"])

        self.save()

        return MainConfig(projectpath=self.projectpath)


class CollectionConfigTemplate(YAMLConfigTemplate, CollectionMixin):
    def __init__(self, projectname=None, files=[], *args, **kw):
        self.projectname = projectname
        self.files = files
        super().__init__(
            "collection.yaml",
            *args,
            **kw,
        )

    def _set_or_initialize_multi_items(
        self, collection_config, key, default_value
    ):
        if collection_config.content and getattr(collection_config, key)():
            getattr(self, key)(value=getattr(collection_config, key)())
        else:
            getattr(self, key)(value=default_value)

    def hits_in_files(self, xpath):
        # all_sources = [self.base] + self.targets
        count = 0
        for tree in self.files:
            if tree.find(xpath) is not None:
                count += 1
        return round((count * 100) / len(self.files), 2)

    def process_proposals(self, attribs, orig_content=None):
        main_config = MainConfig(self.projectpath)

        for attrib in attribs:
            orig_attrib = None
            if orig_content:
                orig_attrib = orig_content.get(attrib)
            if attribs[attrib]:
                attribs[attrib]["value"] = None
                if "proposals" in attribs[attrib]:
                    # we pop out the 'proposals' and we want to remove them
                    # from the config eiterway
                    proposals = attribs[attrib].pop("proposals")
                    if not proposals:
                        continue

                    # init some statistics
                    min_hitrate = main_config.min_hitrate  # in %
                    winner = None
                    for _xpath_prop in proposals:
                        xpath_prop = split_xpath(_xpath_prop)
                        log.debug("[process_proposals] %s" % xpath_prop)
                        hitrate = self.hits_in_files(xpath_prop["xpath"])
                        if hitrate > min_hitrate:
                            winner = xpath_prop["full_path"]
                            min_hitrate = hitrate
                    if winner is not None and "xpath" in attribs[attrib]:
                        log.debug(
                            "[process_proposals] And the winner is `%s` having \
%s percent hitrate"
                            % (winner, min_hitrate)
                        )
                        attribs[attrib]["xpath"] = winner
                else:
                    # ok...there are no proposals at this level
                    # but maybe at the next level, so let's do some
                    # recursion
                    self.process_proposals(
                        attribs[attrib],
                        orig_content=orig_attrib,
                    )

    def render(self, overwrite=False):
        collection_config = CollectionConfig(self.subproject["basepath"])

        if not self.short_title():
            self.short_title(self.subproject["name"])

        if not self.long_title():
            if self.projectname:
                self.long_title(
                    "%s - %s" % (self.projectname, self.subproject["name"])
                )
            else:
                self.long_title(self.short_title())

        for target in self.subproject["files"]:
            self.elements.append(
                {"fullpath": target, "filename": target.split("/")[-1]}
            )

        # running through proposals and set xpath if hitrate is above
        for section in ["attributes", "eltec_specs"]:
            self.process_proposals(
                self.collection[section],
                orig_content=(
                    None
                    if overwrite or not collection_config.content
                    else collection_config.collection[section]
                ),
            )

        for subjects_item in [
            {
                "id": "basic_classifications",
                "default_url": "http://uri.gbv.de/terminology/bk/",
            },
            {
                "id": "gnd_subjects",
                "default_url": "https://d-nb.info/gnd/",
            },
        ]:
            self._set_or_initialize_multi_items(
                collection_config,
                subjects_item["id"],
                [
                    {
                        "id": {"xpath": None, "value": None},
                        "url": {
                            "xpath": None,
                            "value": subjects_item["default_url"],
                        },
                        "value": {"xpath": None, "value": None},
                    }
                ],
            )

        for admin_item in ["rights_holder", "collector"]:
            self._set_or_initialize_multi_items(
                collection_config,
                admin_item,
                [{"fullname": None, "url": None}],
            )

        self.save()

        log.info("%s initialized!" % self.path)
