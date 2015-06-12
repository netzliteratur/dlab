#-*- coding:utf-8 -*-
import sys
import bsz_sru
import uuid
import datetime
from lxml import etree as ET


def fetch_infos_bsz_sru(ppn):
    """
    read sru_bsz.cfg file and
    search and retrieve metadata
    :return string response:
    """
    try:
        user_name, user_passwd = bsz_sru.read_config("config/sru_bsz.cfg")
        response = bsz_sru.search_retrieve(ppn, user_name, user_passwd)

    except IOError, err:
        print("Konnte Metadaten nicht beziehen. Fehlermeldung: \n" +
              str(err))
        sys.exit(1)

    return response


def parse_bsz_sru_infos(response):
    """
    parse response from bsz_sru.search_retrieve
    :return dictionary return_dict:
    """
    return_dict = {}
    author_dict_list = []

    root = ET.fromstring(response)


    if root[1].text != "1":
        print("Kein eindeutiger Datensatz gefunden. Breche ab.")
        sys.exit(0)

    non_sort = ""
    title = ""
    sub_title = ""
    part_name = ""
    part_number = ""

    for child in root[3][0][2][0][0]:
        if child.attrib['id'] == '021A':
            for subfield in child:
                if subfield.attrib['id'] == 'a':
                    if "@" in subfield.text:
                        non_sort = subfield.text.split("@")[0]
                        title = subfield.text.split("@")[1]
                    else:
                        non_sort = ""
                        title = subfield.text
                if subfield.attrib['id'] == 'd':
                    sub_title = subfield.text
                
                if subfield.attrib['id'] == 'h':
                    author_list = subfield.text.split("; ")
                    for element in author_list:
                        print("debug: " + element)
                        author_temp = element.split(" ")
                        if len(author_temp) == 1:
                            family_name = author_temp[0]
                            given_name = ""
                        else:
                            if author_temp[0] == "von":
                                family_name = author_temp[-1]
                                given_name = author_temp[1]
                            else:
                                family_name = author_temp[-1]
                                given_name = author_temp[0]

                        author_dict_list.append({'family': family_name, 'given': given_name})
                
        """if child.attrib['id'] == '028C':
            for subfield in child:
                if subfield.attrib['id'] == '8':
                    print(subfield.text)
                    author_temp = subfield.text.split(",")
                    if len(author_temp) == 1:
                        family_name = author_temp[0]
                        given_name = ""
                    else:
                        if author_temp[0] == "von":
                            family_name = author_temp[-1]
                            given_name = author_temp[1]
                        else:
                            family_name = author_temp[-1]
                            given_name = author_temp[0]

                    author_dict_list.append({'family': family_name, 'given': given_name})
        """

        # lang
        if child.attrib['id'] == '010@':
            language_term = []
            for subfield in child:
                if subfield.attrib['id'] == 'a':
                    language_term.append(subfield.text)

        # origin info
        if child.attrib['id'] == '011@':
            for subfield in child:
                if subfield.attrib['id'] == 'a':
                    date_created = subfield.text

        # part name and part number
        if child.attrib['id'] == '036C':
            for subfield in child:
                part_name = subfield.text

            swap_title_part = title
            title = part_name
            part_name = non_sort + swap_title_part
            non_sort = ""

    return_dict['author_info'] = author_dict_list
    return_dict['origin_info'] = date_created
    return_dict['title_info'] = [non_sort, title, sub_title, part_name, part_number]
    return_dict['language_term'] = language_term

    return_dict['type_of_resource'] = 'mixed material'
    return_dict['genre'] = 'web site'

    return return_dict


def parse_swhwdb(reg_id):
    """
    read dla_swhw.xml file and find
    supported file formats
    :return list sw_list, hw_list:
    """
    tree = ET.parse("config/dla_swhw.xml")
    root = tree.getroot()
    sw_list = []
    hw_list = []

    for swentry in root[1]:
        for child in swentry:
            if child.tag == "swSupportedFormats":
                for format_ in child:
                    if format_.text == reg_id:
                        entry_ = swentry.getchildren()
                        sw_list.append(entry_[0].text)
                        sw_list.append(entry_[1].text)
                        sw_list.append(entry_[2].text)
                        sw_list.append(entry_[3].text)
                        sw_list.append(entry_[4].text)
                        sw_list.append(entry_[5].text)

    if len(sw_list) == 0:
        for n in range(0,5):
            sw_list.append("NONE")

    for hwentry in root[2]:
        hw_entry_ = []
        for child in hwentry:
            hw_entry_.append(child.text)

        hw_list.append(hw_entry_)

    return sw_list, hw_list


def write_metadata_file(temp_dir, sru_dict, add_dict, file_list, rep_list, rep_bool):
    """
    write the metadata.xml file
    """
    creation_date = datetime.datetime.today().isoformat()
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    ET.register_namespace("mets", "http://www.loc.gov/METS/")
    ET.register_namespace("mods", "http://www.loc.gov/mods/v3")
    ET.register_namespace("premis", "info:lc/xmlns/premis-v2")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

    NSMAP = {'mets': 'http://www.loc.gov/METS/',
            'mods': 'http://www.loc.gov/mods/v3',
            'premis': 'info:lc/xmlns/premis-v2',
            'xlink': 'http://www.w3.org/1999/xlink',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
            }
    xsi = "http://www.w3.org/2001/XMLSchema-instance"
    schemaLocation = 'http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/mets.xsd'
    root = ET.Element("{http://www.loc.gov/METS/}mets", nsmap=NSMAP, attrib={"{" + xsi + "}schemaLocation": schemaLocation})

    # METS HEADER
    mets_hdr = ET.SubElement(root, "{http://www.loc.gov/METS/}metsHdr")
    mets_hdr.set("CREATEDATE", creation_date)

    agent = ET.SubElement(mets_hdr, "{http://www.loc.gov/METS/}agent")
    agent.set("ROLE", "CREATOR")
    agent.set("TYPE", "ORGANIZATION")

    mets_name = ET.SubElement(agent, "{http://www.loc.gov/METS/}name")
    mets_name.text = "Deutsches Literaturarchiv Marbach"

    doc_id = uuid.uuid4()
    mets_doc_id = ET.SubElement(mets_hdr, "{http://www.loc.gov/METS/}metsDocumentID")
    mets_doc_id.text = "_" + str(doc_id)

    # dmdSec
    dmdsec_id = uuid.uuid4()
    dmd_sec = ET.SubElement(root, "{http://www.loc.gov/METS/}dmdSec")
    dmd_sec.set("ID", "_" + str(dmdsec_id))

    md_wrap = ET.SubElement(dmd_sec, "{http://www.loc.gov/METS/}mdWrap")
    md_wrap.set("MDTYPE", "MODS")

    xml_data = ET.SubElement(md_wrap, "{http://www.loc.gov/METS/}xmlData")


    schemaLocation = 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd'
    mods = ET.SubElement(xml_data, "{http://www.loc.gov/mods/v3}mods", attrib={"{" + xsi + "}schemaLocation": schemaLocation})
    mods.set("version", "3.5")

    # title
    mods_title_info = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}titleInfo")
    mods_title_info_title = ET.SubElement(mods_title_info, "{http://www.loc.gov/mods/v3}title")
    mods_title_info_title.set("lang", add_dict['title_lang'])
    mods_title_info_title.text = sru_dict['title_info'][1]
    # subtitle
    if sru_dict['title_info'][2] != "":
        mods_title_info_subtitle = ET.SubElement(mods_title_info, "{http://www.loc.gov/mods/v3}subTitle")
        mods_title_info_subtitle.set("lang", add_dict['subtitle_lang'])
        mods_title_info_subtitle.text = sru_dict['title_info'][2]
    # partName and partNumber
    if sru_dict['title_info'][3] != "":
        mods_title_info_part_name = ET.SubElement(mods_title_info, "{http://www.loc.gov/mods/v3}partName")
        mods_title_info_part_name.text = sru_dict['title_info'][3]
    if sru_dict['title_info'][4] != "":
        mods_title_info_part_number = ET.SubElement(mods_title_info, "{http://www.loc.gov/mods/v3}partNumber")
        mods_title_info_part_number.text = sru_dict['title_info'][4]
    # nonsort
    if sru_dict['title_info'][0] != "":
        mods_title_info_nonsort = ET.SubElement(mods_title_info, "{http://www.loc.gov/mods/v3}nonSort")
        mods_title_info_nonsort.set("lang", add_dict['title_lang'])
        mods_title_info_nonsort.text = sru_dict['title_info'][0]
    # name
    author_counter = 0
    for entry in sru_dict['author_info']:
        mods_name = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}name")
        mods_name.set("type", "personal")
        mods_name.set("authorityURI", "http://www.dnb.de/gnd")
        mods_name.set("valueURI", add_dict["gnd_uri_" + str(author_counter)])
        mods_name_name_part = ET.SubElement(mods_name, "{http://www.loc.gov/mods/v3}namePart")
        if entry['given'] != "":
            mods_name_name_part.text = entry['family'] + ", " + entry['given']
        else:
            mods_name_name_part.text = entry['family']
        mods_name_role = ET.SubElement(mods_name, "{http://www.loc.gov/mods/v3}role")
        mods_name_role_term = ET.SubElement(mods_name_role, "{http://www.loc.gov/mods/v3}roleTerm")
        mods_name_role_term.set("type", "text")
        mods_name_role_term.text = "creator"
        author_counter += 1

    # originInfo
    mods_originInfo = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}originInfo")
    mods_originInfo_date_created = ET.SubElement(mods_originInfo, "{http://www.loc.gov/mods/v3}dateCreated")
    mods_originInfo_date_created.set("encoding", "iso8601")
    mods_originInfo_date_created.text = sru_dict['origin_info']

    # location
    mods_location = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}location")
    if add_dict['location_live'] != "":
        mods_location_url = ET.SubElement(mods_location, "{http://www.loc.gov/mods/v3}url")
        mods_location_url.set("displayLabel", "liveweb")
        mods_location_url.text = add_dict['location_live']

    if add_dict['location_archived'] != "":
        mods_location_url = ET.SubElement(mods_location, "{http://www.loc.gov/mods/v3}url")
        mods_location_url.set("displayLabel", "archived")
        mods_location_url.text = add_dict['location_archived']

    # physicalDescription
    mods_physicalDescription = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}physicalDescription")
    mods_physicalDescription_form = ET.SubElement(mods_physicalDescription,
                                                  "{http://www.loc.gov/mods/v3}form")
    mods_physicalDescription_form.set("authority", "marcform")
    mods_physicalDescription_form.text = "electronic"
    mods_physicalDescription_digital_origin = ET.SubElement(mods_physicalDescription,
                                                            "{http://www.loc.gov/mods/v3}digitalOrigin")
    mods_physicalDescription_digital_origin.text = "born digital"

    # abstract
    mods_abstract = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}abstract")
    mods_abstract.set("type", "descriptionByAuthor")
    mods_abstract.text = add_dict['abstract_author'].decode(encoding="utf-8")
    mods_abstract = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}abstract")
    mods_abstract.set("type", "reflectiveDescription")
    mods_abstract.text = add_dict['abstract_reflective'].decode(encoding="utf-8")

    # typeofResource
    mods_type_of_resource = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}typeOfResource")
    mods_type_of_resource.text = sru_dict['type_of_resource']

    # genre
    mods_genre = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}genre")
    mods_genre.set("authority", "marcgt")
    mods_genre.text = sru_dict['genre']

    # language
    mods_language = ET.SubElement(mods, "{http://www.loc.gov/mods/v3}language")
    for lang_entry in sru_dict['language_term']:
        mods_language_term = ET.SubElement(mods_language, "{http://www.loc.gov/mods/v3}languageTerm")
        mods_language_term.set("type", "code")
        mods_language_term.set("authority", "iso639-2b")
        mods_language_term.text = lang_entry

    # AmdSec
    rights_md_uuid = str(uuid.uuid4())

    amd_sec = ET.SubElement(root, "{http://www.loc.gov/METS/}amdSec")


    admid_dict_file = {}
    admid_dict_rep = {}

    # premis
    premis_object_counter_flag = False
    for file_ in file_list:
        # techMD
        file_name_ = file_.keys()[0]
        tech_md_uuid = str(uuid.uuid4())
        admid_dict_file[file_[file_name_]['hash']] = "_" + tech_md_uuid
        tech_md = ET.SubElement(amd_sec, "{http://www.loc.gov/METS/}techMD")
        tech_md.set("ID", "_" + tech_md_uuid)
        
        md_wrap = ET.SubElement(tech_md, "{http://www.loc.gov/METS/}mdWrap")
        md_wrap.set("MDTYPE", "PREMIS:OBJECT")
        xml_data = ET.SubElement(md_wrap, "{http://www.loc.gov/METS/}xmlData")
        if not premis_object_counter_flag:
            schemaLocation = "info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/v2/premis-v2-3.xsd"
            premis_object = ET.SubElement(xml_data,
                                          "{info:lc/xmlns/premis-v2}object", attrib={"{" + xsi + "}schemaLocation": schemaLocation})
            premis_object.set("{http://www.w3.org/2001/XMLSchema-instance}type", "premis:file")
            premis_object_counter_flag = True
        else:
            premis_object = ET.SubElement(xml_data,
                                          "{info:lc/xmlns/premis-v2}object")
            premis_object.set("{http://www.w3.org/2001/XMLSchema-instance}type", "premis:file")
        object_identifier = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}objectIdentifier")
        object_identifier_type = ET.SubElement(object_identifier, "{info:lc/xmlns/premis-v2}objectIdentifierType")
        object_identifier_value = ET.SubElement(object_identifier, "{info:lc/xmlns/premis-v2}objectIdentifierValue")
        object_identifier_type.text = "UUID"
        object_identifier_value.text = file_[file_name_]['uuid']

        object_object_characteristics = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}objectCharacteristics")
        object_object_characteristics_compo_level = ET.SubElement(object_object_characteristics,
                                                                  "{info:lc/xmlns/premis-v2}compositionLevel")
        object_object_characteristics_compo_level.text = "0"
        object_object_characteristics_fixity = ET.SubElement(object_object_characteristics,
                                                             "{info:lc/xmlns/premis-v2}fixity")
        object_object_characteristics_fixity_algo = ET.SubElement(object_object_characteristics_fixity,
                                                                  "{info:lc/xmlns/premis-v2}messageDigestAlgorithm")
        object_object_characteristics_fixity_algo.text = "sha256"
        object_object_characteristics_fixity_digest = ET.SubElement(object_object_characteristics_fixity,
                                                                    "{info:lc/xmlns/premis-v2}messageDigest")
        object_object_characteristics_fixity_digest.text = file_[file_name_]['hash']
        object_object_characteristics_size = ET.SubElement(object_object_characteristics,
                                                           "{info:lc/xmlns/premis-v2}size")
        object_object_characteristics_size.text = str(file_[file_name_]['file_size'])

        object_object_characteristics_format = ET.SubElement(object_object_characteristics,
                                                             "{info:lc/xmlns/premis-v2}format")

        object_object_characteristics_format_design = ET.SubElement(object_object_characteristics_format,
                                                                    "{info:lc/xmlns/premis-v2}formatDesignation")
        object_object_characteristics_format_design_name = ET.SubElement(object_object_characteristics_format_design,
                                                                         "{info:lc/xmlns/premis-v2}formatName")
        object_object_characteristics_format_design_name.text = file_[file_name_]['format_name']
        object_object_characteristics_format_design_version = ET.SubElement(object_object_characteristics_format_design,
                                                                            "{info:lc/xmlns/premis-v2}formatVersion")
        object_object_characteristics_format_design_version.text = ""

        object_object_characteristics_format_registry = ET.SubElement(object_object_characteristics_format,
                                                                      "{info:lc/xmlns/premis-v2}formatRegistry")

        object_object_characteristics_format_registry_name = ET.SubElement(object_object_characteristics_format_registry,
                                                                           "{info:lc/xmlns/premis-v2}formatRegistryName")
        object_object_characteristics_format_registry_name.text = "PRONOM"

        object_object_characteristics_format_registry_key = ET.SubElement(object_object_characteristics_format_registry,
                                                                          "{info:lc/xmlns/premis-v2}formatRegistryKey")
        object_object_characteristics_format_registry_key.text = file_[file_name_]['format_registry_key']


        object_storage = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}storage")

        object_storage_location = ET.SubElement(object_storage, "{info:lc/xmlns/premis-v2}contentLocation")
        object_storage_location_type = ET.SubElement(object_storage_location,
                                                     "{info:lc/xmlns/premis-v2}contentLocationType")
        object_storage_location_type.text = "Path"
        object_storage_location_value = ET.SubElement(object_storage_location,
                                                      "{info:lc/xmlns/premis-v2}contentLocationValue")
        object_storage_location_value.text = file_[file_name_]['path']


        object_environment = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}environment")
        object_environment_env_char = ET.SubElement(object_environment,
                                                    "{info:lc/xmlns/premis-v2}environmentCharacteristic")
        object_environment_env_char.text = "known to work"
        object_environment_env_purpose = ET.SubElement(object_environment,
                                                       "{info:lc/xmlns/premis-v2}environmentPurpose")

        if file_[file_name_]['format_name'] == '"GZIP Format"':
            object_environment_env_purpose.text = "extract"
        elif file_[file_name_]['format_name'] == '"ZIP Format"':
            object_environment_env_purpose.text = "extract"
        else:
            object_environment_env_purpose.text = "render"

        reg_id_ = file_[file_name_]['format_registry_key']
        env_list, hw_list = parse_swhwdb(reg_id_)

        object_environment_software = ET.SubElement(object_environment, "{info:lc/xmlns/premis-v2}software")
        object_environment_software_sw_name = ET.SubElement(object_environment_software,
                                                            "{info:lc/xmlns/premis-v2}swName")
        object_environment_software_sw_name.text = env_list[0] + " ; " + env_list[1]


        object_environment_software_sw_version = ET.SubElement(object_environment_software,
                                                               "{info:lc/xmlns/premis-v2}swVersion")
        object_environment_software_sw_version.text = env_list[2]

        object_environment_software_sw_type = ET.SubElement(object_environment_software,
                                                            "{info:lc/xmlns/premis-v2}swType")

        object_environment_software_sw_type.text = env_list[3]

        #object_environment_software_sw_dependency = ET.SubElement(object_environment_software,
        #                                                          "{info:lc/xmlns/premis-v2}swDependency")

        #object_environment_software_sw_dependency.text = env_list[4]

        for hw_entry in hw_list:
            object_environment_hardware = ET.SubElement(object_environment, "{info:lc/xmlns/premis-v2}hardware")
            object_environment_hardware_hw_name = ET.SubElement(object_environment_hardware,
                                                                "{info:lc/xmlns/premis-v2}hwName")

            object_environment_hardware_hw_name.text = hw_entry[0] + " ; " + hw_entry[1]

            object_environment_hardware_hw_type = ET.SubElement(object_environment_hardware,
                                                                "{info:lc/xmlns/premis-v2}hwType")

            object_environment_hardware_hw_type.text = hw_entry[2]

            #object_environment_hardware_hw_other_info = ET.SubElement(object_environment_hardware,
            #                                                          "{info:lc/xmlns/premis-v2}hwOtherInformation")

            # TODO for other info repeat
            #object_environment_hardware_hw_other_info.text = "test"

        object_relationship = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}relationship")
        object_relationship_type = ET.SubElement(object_relationship, "{info:lc/xmlns/premis-v2}relationshipType")
        object_relationship_type.text = "structural"
        object_relationship_subtype = ET.SubElement(object_relationship,
                                                    "{info:lc/xmlns/premis-v2}relationshipSubType")
        object_relationship_subtype.text = 'is part of'

        object_relationship_obj_id = ET.SubElement(object_relationship,
                                                   "{info:lc/xmlns/premis-v2}relatedObjectIdentification")
        object_relationship_obj_id_type = ET.SubElement(object_relationship_obj_id,
                                                        "{info:lc/xmlns/premis-v2}relatedObjectIdentifierType")
        object_relationship_obj_id_type.text = "UUID"
        object_relationship_obj_id_value = ET.SubElement(object_relationship_obj_id,
                                                        "{info:lc/xmlns/premis-v2}relatedObjectIdentifierValue")
        object_relationship_obj_id_value.text = file_[file_name_]['is_part']

    screenshot_rep_has = []
    screenshot_rep_is = ""
    for rep_ in rep_list:
        rep_name_ = rep_.keys()[0]
        cat_ = rep_[rep_name_]['cat']
        if cat_ == 'screenshot':
            screenshot_rep_is = rep_[rep_name_]['uuid']
            screenshot_rep_has.append(rep_[rep_name_]['has_part'])
        else:
            # techMD
            tech_md_uuid = str(uuid.uuid4())
            admid_dict_rep[rep_[rep_name_]['cat']] = "_" + tech_md_uuid
            tech_md = ET.SubElement(amd_sec, "{http://www.loc.gov/METS/}techMD")
            tech_md.set("ID", "_" + tech_md_uuid)
            md_wrap = ET.SubElement(tech_md, "{http://www.loc.gov/METS/}mdWrap")
            md_wrap.set("MDTYPE", "PREMIS:OBJECT")
            xml_data = ET.SubElement(md_wrap, "{http://www.loc.gov/METS/}xmlData")

            premis_object = ET.SubElement(xml_data,
                                          "{info:lc/xmlns/premis-v2}object")
            premis_object.set("{http://www.w3.org/2001/XMLSchema-instance}type", "premis:representation")

            object_identifier = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}objectIdentifier")
            object_identifier_type = ET.SubElement(object_identifier, "{info:lc/xmlns/premis-v2}objectIdentifierType")
            object_identifier_value = ET.SubElement(object_identifier, "{info:lc/xmlns/premis-v2}objectIdentifierValue")
            object_identifier_type.text = "UUID"
            object_identifier_value.text = rep_[rep_name_]['uuid']

            object_environment = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}environment")
            object_environment_env_char = ET.SubElement(object_environment,
                                                        "{info:lc/xmlns/premis-v2}environmentCharacteristic")
            object_environment_env_char.text = "known to work"
            object_environment_env_purpose = ET.SubElement(object_environment, "{info:lc/xmlns/premis-v2}environmentPurpose")
            object_environment_env_purpose.text = "render"

            if rep_[rep_name_]['cat'] == 'crawl':
                sw_name = "Internet Archive ; wayback"
                sw_version = "1.6.0"
                sw_type = "server"
                sw_dep = ""
            elif rep_[rep_name_]['cat'] == 'screenshot':
                sw_name = "Daniel Friesel ; feh"
                sw_version = "2.12"
                sw_type = "renderer"
                sw_dep = ""
            elif rep_[rep_name_]['cat'] == 'screencast':
                sw_name = "vlc"
                sw_version = "2.1.5"
                sw_type = "renderer"
                sw_dep = ""
            else:
                sw_name = "UNSPEC"
                sw_version = "UNSPEC"
                sw_type = "UNSPEC"
                sw_dep = "UNSPEC"

            # software
            if rep_[rep_name_]['cat'] != "source":
                object_environment_software = ET.SubElement(object_environment, "{info:lc/xmlns/premis-v2}software")
                object_environment_software_sw_name = ET.SubElement(object_environment_software,
                                                                "{info:lc/xmlns/premis-v2}swName")
                object_environment_software_sw_name.text = sw_name

                object_environment_software_sw_version = ET.SubElement(object_environment_software,
                                                                        "{info:lc/xmlns/premis-v2}swVersion")
                object_environment_software_sw_version.text = sw_version

                object_environment_software_sw_type = ET.SubElement(object_environment_software,
                                                                   "{info:lc/xmlns/premis-v2}swType")

                object_environment_software_sw_type.text = sw_type

                #if sw_dep != "":
                #    object_environment_software_sw_dependency = ET.SubElement(object_environment_software,
                #                                                        "{info:lc/xmlns/premis-v2}swDependency")
                #    object_environment_software_sw_dependency.text = sw_dep

                # hardware
                # No hardware in representations
                #object_environment_hardware = ET.SubElement(object_environment, "{info:lc/xmlns/premis-v2}hardware")
                #object_environment_hardware_hw_name = ET.SubElement(object_environment_hardware,
                #                                                    "{info:lc/xmlns/premis-v2}hwName")
                #object_environment_hardware_hw_type = ET.SubElement(object_environment_hardware,
                #                                                    "{info:lc/xmlns/premis-v2}hwType")
                #object_environment_hardware_hw_other_info = ET.SubElement(object_environment_hardware,
                #                                                      "{info:lc/xmlns/premis-v2}hwOtherInformation")

            object_relationship = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}relationship")
            object_relationship_type = ET.SubElement(object_relationship, "{info:lc/xmlns/premis-v2}relationshipType")
            object_relationship_type.text = "structural"
            object_relationship_subtype = ET.SubElement(object_relationship,
                                                        "{info:lc/xmlns/premis-v2}relationshipSubType")
            object_relationship_subtype.text = 'has part'

            object_relationship_obj_id = ET.SubElement(object_relationship,
                                                       "{info:lc/xmlns/premis-v2}relatedObjectIdentification")
            object_relationship_obj_id_type = ET.SubElement(object_relationship_obj_id,
                                                            "{info:lc/xmlns/premis-v2}relatedObjectIdentifierType")
            object_relationship_obj_id_type.text = "UUID"
            object_relationship_obj_id_value = ET.SubElement(object_relationship_obj_id,
                                                            "{info:lc/xmlns/premis-v2}relatedObjectIdentifierValue")

            try:
                object_relationship_obj_id_value.text = rep_[rep_name_]['has_part']
            except KeyError as e:
                print("Representation gefunden, aber keine zugehörigen Dateien. "
                      "Eventuell fehlen Screenshots. Siehe Spezifikation im Doc-Verzeichnis.")

    # screenshot
    # techMD
    tech_md_uuid = str(uuid.uuid4())
    admid_dict_rep['screenshots'] = "_" + tech_md_uuid
    tech_md = ET.SubElement(amd_sec, "{http://www.loc.gov/METS/}techMD")
    tech_md.set("ID", "_" + tech_md_uuid)
    md_wrap = ET.SubElement(tech_md, "{http://www.loc.gov/METS/}mdWrap")
    md_wrap.set("MDTYPE", "PREMIS:OBJECT")
    xml_data = ET.SubElement(md_wrap, "{http://www.loc.gov/METS/}xmlData")
    premis_object = ET.SubElement(xml_data,
                                  "{info:lc/xmlns/premis-v2}object")
    premis_object.set("{http://www.w3.org/2001/XMLSchema-instance}type", "premis:representation")

    object_identifier = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}objectIdentifier")
    object_identifier_type = ET.SubElement(object_identifier, "{info:lc/xmlns/premis-v2}objectIdentifierType")
    object_identifier_value = ET.SubElement(object_identifier, "{info:lc/xmlns/premis-v2}objectIdentifierValue")
    object_identifier_type.text = "UUID"
    object_identifier_value.text = screenshot_rep_is

    object_environment = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}environment")
    object_environment_env_char = ET.SubElement(object_environment, "{info:lc/xmlns/premis-v2}environmentCharacteristic")
    object_environment_env_char.text = "known to work"
    object_environment_env_purpose = ET.SubElement(object_environment, "{info:lc/xmlns/premis-v2}environmentPurpose")
    object_environment_env_purpose.text = "render"
    object_environment_software = ET.SubElement(object_environment, "{info:lc/xmlns/premis-v2}software")

    object_environment_software_sw_name = ET.SubElement(object_environment_software,
                                                        "{info:lc/xmlns/premis-v2}swName")

    object_environment_software_sw_name.text = "Daniel Friesel ; feh"

    object_environment_software_sw_version = ET.SubElement(object_environment_software,
                                                           "{info:lc/xmlns/premis-v2}swVersion")
    object_environment_software_sw_version.text = "2.12"

    object_environment_software_sw_type = ET.SubElement(object_environment_software,
                                                        "{info:lc/xmlns/premis-v2}swType")
    object_environment_software_sw_type.text = "renderer"

    #if sw_dep != "":
    #    object_environment_software_sw_dependency = ET.SubElement(object_environment_software,
    #                                                              "{info:lc/xmlns/premis-v2}swDependency")

    #    object_environment_software_sw_dependency.text = sw_dep

    # hardware
    # No hardware in screenshot representations

    object_relationship = ET.SubElement(premis_object, "{info:lc/xmlns/premis-v2}relationship")
    object_relationship_type = ET.SubElement(object_relationship, "{info:lc/xmlns/premis-v2}relationshipType")
    object_relationship_type.text = "structural"
    object_relationship_subtype = ET.SubElement(object_relationship,
                                                "{info:lc/xmlns/premis-v2}relationshipSubType")
    object_relationship_subtype.text = 'has part'

    for object_ in screenshot_rep_has:
        object_relationship_obj_id = ET.SubElement(object_relationship, "{info:lc/xmlns/premis-v2}"
                                                                        "relatedObjectIdentification")
        object_relationship_obj_id_type = ET.SubElement(object_relationship_obj_id, "{info:lc/xmlns/premis-v2}"
                                                                                    "relatedObjectIdentifierType")
        object_relationship_obj_id_type.text = "UUID"
        object_relationship_obj_id_value = ET.SubElement(object_relationship_obj_id, "{info:lc/xmlns/premis-v2}"
                                                                                     "relatedObjectIdentifierValue")
        object_relationship_obj_id_value.text = object_

    # rightsMD
    rights_md = ET.SubElement(amd_sec, "{http://www.loc.gov/METS/}rightsMD")
    rights_md.set("ID", "_" + rights_md_uuid)
    rights_md_wrap = ET.SubElement(rights_md, "{http://www.loc.gov/METS/}mdWrap")
    rights_md_wrap.set("MDTYPE", "MODS")
    rights_md_xml_data = ET.SubElement(rights_md_wrap, "{http://www.loc.gov/METS/}xmlData")
    rights_md_mods = ET.SubElement(rights_md_xml_data, "{http://www.loc.gov/mods/v3}mods")
    rights_md_mods.set("version", "3.5")
    rights_md_access = ET.SubElement(rights_md_mods, "{http://www.loc.gov/mods/v3}accessCondition")
    rights_md_access.set("type", "restriction on access")
    access_condition = add_dict['access_condition']
    if access_condition.lower() == "moving wall":
        moving_wall_date = " frei ab " + add_dict['moving_wall_date']
    else:
        moving_wall_date = ""
    rights_md_access.text = access_condition + moving_wall_date

    for rightsholder in add_dict['rights_holder']:
        rights_md_holder = ET.SubElement(rights_md_mods, "{http://www.loc.gov/mods/v3}accessCondition")
        rights_md_holder.set("type", "use and reproduction")
        rights_md_holder.text = rightsholder

    # fileSec
    file_sec_uuid = str(uuid.uuid4())
    file_sec = ET.SubElement(root, "{http://www.loc.gov/METS/}fileSec")
    file_sec.set("ID", "_" + file_sec_uuid)
    if rep_bool['crawl']:
        file_sec_crawl = ET.SubElement(file_sec, "{http://www.loc.gov/METS/}fileGrp")
        file_sec_crawl.set("USE", "crawl")
    if rep_bool['screencast']:
        file_sec_screencast = ET.SubElement(file_sec, "{http://www.loc.gov/METS/}fileGrp")
        file_sec_screencast.set("USE", "screencast")
    if rep_bool['source code']:
        file_sec_source_code = ET.SubElement(file_sec, "{http://www.loc.gov/METS/}fileGrp")
        file_sec_source_code.set("USE", "source code")
    if rep_bool['screenshot']:
        file_sec_screenshot = ET.SubElement(file_sec, "{http://www.loc.gov/METS/}fileGrp")
        file_sec_screenshot.set("USE", "screenshot")

    # structMap
    struct_map = ET.SubElement(root, "{http://www.loc.gov/METS/}structMap")
    struct_map.set("ID", "_" + str(uuid.uuid4()))
    set_screenshot_ = False
    set_screencast_ = False

    struct_map_extra_div = ET.SubElement(struct_map, "{http://www.loc.gov/METS/}div")

    for file_ in file_list:
        file_name_ = file_.keys()[0]
        if file_name_.startswith('crawl_'):
            file_sec_file = ET.SubElement(file_sec_crawl, "{http://www.loc.gov/METS/}file")
            file_sec_file_flocat = ET.SubElement(file_sec_file, "{http://www.loc.gov/METS/}FLocat")
            file_sec_file.set("ID", file_[file_name_]['uuid'])
            file_sec_file.set("CREATED", file_[file_name_]['date_created'])
            file_sec_file.set("ADMID", admid_dict_file[file_[file_name_]['hash']])
            file_sec_file_flocat.set("LOCTYPE", "OTHER")
            file_sec_file_flocat.set("OTHERLOCTYPE", "Path")
            file_sec_file_flocat.set("{http://www.w3.org/1999/xlink}href", file_[file_name_]['path'])

            struct_map_div = ET.SubElement(struct_map_extra_div, "{http://www.loc.gov/METS/}div")
            struct_map_div.set("TYPE", "crawl")
            struct_map_div.set("ADMID", admid_dict_rep['crawl'])
            struct_map_fptr = ET.SubElement(struct_map_div, "{http://www.loc.gov/METS/}fptr")
            struct_map_fptr.set("FILEID", file_[file_name_]['uuid'])

        if file_name_.startswith('source_'):
            file_sec_file = ET.SubElement(file_sec_source_code, "{http://www.loc.gov/METS/}file")
            file_sec_file_flocat = ET.SubElement(file_sec_file, "{http://www.loc.gov/METS/}FLocat")
            file_sec_file.set("ID", file_[file_name_]['uuid'])
            file_sec_file.set("CREATED", file_[file_name_]['date_created'])
            file_sec_file.set("ADMID", admid_dict_file[file_[file_name_]['hash']])
            file_sec_file_flocat.set("LOCTYPE", "OTHER")
            file_sec_file_flocat.set("OTHERLOCTYPE", "Path")
            file_sec_file_flocat.set("{http://www.w3.org/1999/xlink}href", file_[file_name_]['path'])

            struct_map_div = ET.SubElement(struct_map_extra_div, "{http://www.loc.gov/METS/}div")
            struct_map_div.set("TYPE", "source code")
            struct_map_div.set("ADMID", admid_dict_rep['source'])
            struct_map_fptr = ET.SubElement(struct_map_div, "{http://www.loc.gov/METS/}fptr")
            struct_map_fptr.set("FILEID", file_[file_name_]['uuid'])

        if file_name_.startswith('screencast_'):
            file_sec_file = ET.SubElement(file_sec_screencast, "{http://www.loc.gov/METS/}file")
            file_sec_file_flocat = ET.SubElement(file_sec_file, "{http://www.loc.gov/METS/}FLocat")
            file_sec_file.set("ID", file_[file_name_]['uuid'])
            file_sec_file.set("CREATED", file_[file_name_]['date_created'])
            file_sec_file.set("ADMID", admid_dict_file[file_[file_name_]['hash']])
            file_sec_file_flocat.set("LOCTYPE", "OTHER")
            file_sec_file_flocat.set("OTHERLOCTYPE", "Path")
            file_sec_file_flocat.set("{http://www.w3.org/1999/xlink}href", file_[file_name_]['path'])

            #if not set_screencast_:
            #    struct_map_div_screencast = ET.SubElement(struct_map_extra_div, "{http://www.loc.gov/METS/}div")
            #    struct_map_div_screencast.set("TYPE", "screencast")
            #    struct_map_div_screencast.set("ADMID", admid_dict_rep['screencast'])
            #    set_screencast_ = True

            #struct_map_fptr = ET.SubElement(struct_map_div_screencast, "{http://www.loc.gov/METS/}fptr")
            #struct_map_fptr.set("FILEID", file_[file_name_]['uuid'])

            struct_map_div_screencast = ET.SubElement(struct_map_extra_div, "{http://www.loc.gov/METS/}div")
            struct_map_div_screencast.set("TYPE", "screencast")
            struct_map_div_screencast.set("ADMID", admid_dict_rep['screencast'])

            struct_map_fptr = ET.SubElement(struct_map_div_screencast, "{http://www.loc.gov/METS/}fptr")
            struct_map_fptr.set("FILEID", file_[file_name_]['uuid'])

        if file_name_.startswith('screenshot'):
            file_sec_file = ET.SubElement(file_sec_screenshot, "{http://www.loc.gov/METS/}file")
            file_sec_file_flocat = ET.SubElement(file_sec_file, "{http://www.loc.gov/METS/}FLocat")

            file_sec_file.set("ID", file_[file_name_]['uuid'])
            file_sec_file.set("CREATED", file_[file_name_]['date_created'])
            file_sec_file.set("ADMID", admid_dict_file[file_[file_name_]['hash']])
            file_sec_file_flocat.set("LOCTYPE", "OTHER")
            file_sec_file_flocat.set("OTHERLOCTYPE", "Path")
            file_sec_file_flocat.set("{http://www.w3.org/1999/xlink}href", file_[file_name_]['path'])

            if not set_screenshot_:

                struct_map_div_screenshot = ET.SubElement(struct_map_extra_div, "{http://www.loc.gov/METS/}div")
                struct_map_div_screenshot.set("ADMID", admid_dict_rep['screenshots'])
                struct_map_div_screenshot.set("TYPE", "screenshot")
                set_screenshot_ = True

            struct_map_fptr = ET.SubElement(struct_map_div_screenshot, "{http://www.loc.gov/METS/}fptr")
            struct_map_fptr.set("FILEID", file_[file_name_]['uuid'])

    # write metadata.xml
    tree = ET.ElementTree(root)
    tree.write(temp_dir + "/metadata.xml",  encoding="UTF-8", pretty_print=True, xml_declaration=True)
