import os
import math
import subprocess
import shutil
from pypers.utils import utils
#import xml.etree.ElementTree as ET
#import xml.dom.minidom as md
from lxml import etree
#from pypers.utils.xmldom import clean_xmlfile
#from pypers.utils.utils import which
from pypers.steps.base.extract import ExtractBase


class Trademarks(ExtractBase):
    """
    Extract PHTM archives
    """
    spec = {
        "version": "2.0",
        "descr": [
            "Returns the directory with the extraction"
        ]
    }

    def preprocess(self):
        self.counter_xml = 0
        self.data_files = {}
        self.img_files = {}
        self.media_files = {}
        # self.archives is a tuple of (date, {archive_name: xxx, archives[]})

        if not len(self.archives):
            return

        extraction_date = self.archives[0]
        archive_name = self.archives[1]['name']
        archives = self.archives[1]['archives']
        # prepare destination dir under pipeline scratch dir
        self.extraction_dir = os.path.join(
            self.meta['pipeline']['output_dir'],
            '__scratch',
            extraction_date,
            archive_name
        )

        # deletes the directory if prev exists
        utils.mkdir_force(self.extraction_dir)

        xml_dir = os.path.join(self.extraction_dir, 'xml')
        os.makedirs(xml_dir, exist_ok=True)

        self.manifest = {'archive_name': archive_name,
                         'archive_file': archive_name,
                         'archive_date': extraction_date,
                         'extraction_dir': self.extraction_dir,
                         'data_files': {},
                         'img_files': {},
                         'media_files': {}}
        for archive in archives:
            self.collect_files(self.unpack_archive(archive, os.path.join(self.extraction_dir, os.path.basename(archive))))

    def add_xml_file(self, filename, fullpath):
        self.logger.info('\nprocessing file: %s' % (fullpath))

        xml_dir = os.path.join(self.extraction_dir, 'xml')

        #clean_xmlfile(fullpath, readenc='utf-16le', writeenc='utf-8', overwrite=True)

        # sometimes it happens that we get
        # an empty update. ex: 20151225
        with open(fullpath, 'r') as fh:
            lines = fh.readlines()
            if len(lines) < 1:
                return

        parser = etree.XMLParser(ns_clean=True, dtd_validation=False, load_dtd=False, no_network=True, recover=True, encoding='utf-8')
        xml_root = None
        try:
            xml_root = etree.parse(fullpath, parser=parser)
        except Exception as e: 
            self.logger.error("XML parsing failed for %s: %s" % (fullpath, e))

        if xml_root == None:
            return

        nss = { "tmk": "http://www.wipo.int/standards/XMLSchema/trademarks", "wo": "http://www.wipo.int/standards/XMLSchema/wo-trademarks" }
        appnum_nodes = xml_root.xpath("//tmk:TradeMark/tmk:ApplicationNumber/text()", namespaces=nss)
        if appnum_nodes != None and len(appnum_nodes)>0:
            appnum = appnum_nodes[0]

            # sanitize appnum : S/123(8) -> S123-8
            appnum = appnum.replace('/', '').replace('-', '').replace('(', '-').replace(')', '')

            print(appnum)

            app_file = os.path.join(xml_dir, '%s.xml' % (appnum))
            #with codecs.open(app_file, 'w', 'utf-8') as fh:
            #    fh.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            #    fh.write(etree.tostring(trademark_node, pretty_print=True).decode("utf-8"))

            shutil.copyfile(fullpath, app_file)

            self.manifest['data_files'].setdefault(appnum, {})
            self.manifest['data_files'][appnum]['ori'] = os.path.relpath(
                app_file, self.extraction_dir
            )

            img_nodes = xml_root.xpath("//tmk:TradeMark//tmk:MarkImage", namespaces=nss)
            for img_node in img_nodes:         
                img_node_filename = img_node.xpath("./tmk:MarkImageFilename/text()", namespaces=nss)
                img_format_node = img_node.xpath("./tmk:MarkImageFileFormat/text()", namespaces=nss)

                if img_node_filename and len(img_node_filename)>0:
                    img_node_filename = img_node_filename[0]

                if img_format_node and len(img_format_node)>0:
                    img_format_node = img_format_node[0]

                if img_format_node and img_node_filename.find(".") == -1:
                    img_node_filename = img_node_filename+"."+img_format_node.lower()

                print(img_node_filename)

                img_file = os.path.join(os.path.dirname(fullpath), img_node_filename)
                print(img_file)

                if img_file:
                    self.add_img_file(appnum, img_file)

            #self.manifest['data_files'].setdefault(appnum, {})
            #self.manifest['data_files'][appnum]['ori'] = os.path.relpath(
            #    tmxml_file, self.extraction_dir
            #)
        # remove the file when done with it
        os.remove(fullpath)


    def process(self):
        pass

