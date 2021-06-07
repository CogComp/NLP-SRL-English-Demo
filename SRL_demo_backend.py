import cherrypy
import os
import json
import requests
import tabular

import sys
import hashlib
import cacheSRL
from xml.dom import minidom

# I bought a book and gave it to him.

# font-family: Lato, 'Lucida Grande', Tahoma, 'Helvetica Neue', Helvetica, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';

BASE_HTML_PATH = "./SRL_html"
BASE_NER_HTTP = "http://dickens.seas.upenn.edu:4022/ner"
BASE_SRL_HTTP = "http://dickens.seas.upenn.edu:4039/annotate"

cache = cacheSRL.CacheSRL()
cache_dic = cache.load()

def getBasicAnnotations(text):
    '''
    # input = {"task":"mention_detection","text":text}
    input = {"task":"kairos_ner","text":text}
    # res_out = requests.get(BASE_KAIROS_NER_HTTP, params = input)
    res_out_NER = requests.post(BASE_KAIROS_NER_HTTP,json=input)
    # print(res_out)
    res_json_NER = res_out_NER.json()
    #print("----------")
    #print(res_json_NER)
    #print("----------")
    '''
    # SRL
    input = {"sentence":text}
    res_out_SRL = requests.post(BASE_SRL_HTTP, json = input)
    res_json_SRL = res_out_SRL.json()
    tokens = []
    endPositions = []
    if "tokens" in res_json_SRL:
        tokens = res_json_SRL["tokens"]
    # print(tokens)
    if "sentences" in res_json_SRL:
        sentences = res_json_SRL["sentences"]
        if "sentenceEndPositions" in sentences:
            endPositions = sentences["sentenceEndPositions"]
    return tokens, endPositions, res_json_SRL

def initView(myTabularView, text, tokens, end_pos):
    myTabularView.setText(text) 
    # t,s,annjsonNER,annjsonSRL = getBasicAnnotations(text)
    # t,s,annjsonSRL = getBasicAnnotations(text) 
    # t,s,annjsonEvents = getBasicAnnotationsFromEVENTS(text)
    myTabularView.setTokens( tokens )
    myTabularView.setSentenceEnds( end_pos )
    #print("====")
    #print(annjson["tokens"])
    #print("====")
    '''
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addSpanLabelView(annjson,"NER_CONLL","NER-CONLL")
    '''
    # return annjsonEvents
    #return annjsonSRL


# def processSRL(myTabularView,text):
def processSRL(myTabularView,annjson):
    # annjson = getSRL(text)
    if "tokens" in annjson:
        tokens = annjson["tokens"]
        # if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addPredicateArgumentView(annjson,"SRL_ONTONOTES","SRL-Verb")
        # myTabularView.addPredicateArgumentView(annjson,"SRL_NOM","SRL-Nom")
        myTabularView.addPredicateArgumentView(annjson,"SRL_NOM_ALL","SRL-Nom")
        myTabularView.addPredicateArgumentView(annjson,"PREPOSITION_SRL","SRL-Prep")

def doProcess(myTabularView, text=None, anns=None):
    
    global cache_dic

    eventsOutput = None
    myTabularView.reset()
    hash_value = hashlib.sha1(text.encode()).hexdigest()

    if cache.count(cache_dic) > 100:
        cache.write(cache_dic)
        cache_dic = cache.load()

    if hash_value in cache_dic['eng'].keys():
        tokens, end_pos, annjsonSRL, cache_dic = cache.read(cache_dic, hash_value, lang='eng')
      
        initView(myTabularView, text, tokens, end_pos)
        processSRL(myTabularView, annjsonSRL)

    else:
        tokens, end_pos, annjsonSRL = getBasicAnnotations(text)
        initView(myTabularView, text, tokens, end_pos)
        processSRL(myTabularView, annjsonSRL)

        cache_dic = cache.add(text,hash_value, tokens, end_pos, annjsonSRL, cache_dic, lang='eng')

    return myTabularView.HTML()

'''
>>> node.
node.ATTRIBUTE_NODE               node.TEXT_NODE                    node.getElementsByTagNameNS(      node.localName                    node.removeAttribute(             node.setIdAttribute(
node.CDATA_SECTION_NODE           node.appendChild(                 node.getInterface(                node.namespaceURI                 node.removeAttributeNS(           node.setIdAttributeNS(
node.COMMENT_NODE                 node.attributes                   node.getUserData(                 node.nextSibling                  node.removeAttributeNode(         node.setIdAttributeNode(
node.DOCUMENT_FRAGMENT_NODE       node.childNodes                   node.hasAttribute(                node.nodeName                     node.removeAttributeNodeNS(       node.setUserData(
node.DOCUMENT_NODE                node.cloneNode(                   node.hasAttributeNS(              node.nodeType                     node.removeChild(                 node.tagName
node.DOCUMENT_TYPE_NODE           node.firstChild                   node.hasAttributes(               node.nodeValue                    node.replaceChild(                node.toprettyxml(
node.ELEMENT_NODE                 node.getAttribute(                node.hasChildNodes(               node.normalize(                   node.schemaType                   node.toxml(
node.ENTITY_NODE                  node.getAttributeNS(              node.insertBefore(                node.ownerDocument                node.setAttribute(                node.unlink(
node.ENTITY_REFERENCE_NODE        node.getAttributeNode(            node.isSameNode(                  node.parentNode                   node.setAttributeNS(              node.writexml(
node.NOTATION_NODE                node.getAttributeNodeNS(          node.isSupported(                 node.prefix                       node.setAttributeNode(
node.PROCESSING_INSTRUCTION_NODE  node.getElementsByTagName(        node.lastChild                    node.previousSibling              node.setAttributeNodeNS(
'''

exampleNumber = 0

def processXMLVerbNode(node):
    global exampleNumber
    htmlNode = ""
    if node.nodeName.lower() in ["frameset","predicate","roleset","roles","role","example","arg","rel","text"]:
        # print(node.nodeName, node.nodeType)
        
        if node.nodeName.lower() == "roleset":
            htmlNode = "<h3>" + node.getAttribute('id') + ": " + node.getAttribute('name') + "</h3>"
            if node.hasAttribute('vncls') and node.getAttribute('vncls') != "-":
                htmlNode += "<h5>" + "verb class" + ": " + node.getAttribute('vncls') + "</h5>"
        
        if node.nodeName.lower() == "roles":
            htmlNode = '<table class="w3-medium" cellspacing=0 width="100%">' 

        if node.nodeName.lower() == "role":
            htmlNode = '<tr><td width=100 style="border-top: 1px solid #C0C0C0;">'+"A"+node.getAttribute('n').upper()+'</td><td style="border-top: 1px solid #C0C0C0;">'+node.getAttribute('descr')+'</td></tr>' 

        if node.nodeName.lower() == "example":
            exampleNumber += 1
            htmlNode  = '<div class="w3-border w3-border-blue w3-round-medium">' 
            htmlNode += '<table class="w3-medium" cellspacing=0 width="100%">' 
            htmlNode += '<tr style="color: #31708f; background-color: #d9edf7;"><td style="border-color: #bce8f1;" colspan="2"><h5>Example '+str(exampleNumber)+'</h5></td></tr>' 
            htmlNode += '</table>' 
            # htmlNode += '<div style="color: #31708f; background-color: #d9edf7; border-color: #bce8f1;"><h5>Example '+str(exampleNumber)+'</h5></div>'
            # htmlNode += '<table class="w3-medium" cellspacing=0 width="100%">' 

        if node.nodeName.lower() == "text":
            # htmlNode = "<tr valign='top'><td colspan='2'><h6>"+node.firstChild.nodeValue+"</h6></td></tr>";
            try:
                htmlNode = "<div class='w3-margin-right w3-margin-left'><h6>"+node.firstChild.nodeValue+"</h6></div>";
            except AttributeError:
                htmlNode = "<div class='w3-margin-right w3-margin-left'><h6>"+"N/A"+"</h6></div>";
            htmlNode += '<div class="w3-panel"><table class="w3-medium" cellspacing=0 width="100%">' 


        if node.nodeName.lower() == "rel":
            arg = "V"
            # htmlNode = "<tr valign='top'><td width=100><h6>"+arg+"</h5></td><td><h6>&nbsp;</h5></td></tr>";
            try:
                htmlNode = '<tr><td width=100 style="border-top: 1px solid #C0C0C0;">'+arg+'</td><td style="border-top: 1px solid #C0C0C0;">'+node.firstChild.nodeValue+'</td></tr>'
            except AttributeError:
                htmlNode = '<tr><td width=100 style="border-top: 1px solid #C0C0C0;">'+arg+'</td><td style="border-top: 1px solid #C0C0C0;">'+"N/A"+'</td></tr>'
            
        if node.nodeName.lower() == "arg":
            arg = "A" + node.getAttribute('n').upper()
            if node.getAttribute('n') == "M" and node.hasAttribute('f') and node.getAttribute('f'):
                arg += "-"+node.getAttribute('f').upper()
            #htmlNode = "<tr valign='top'><td width=100><h6>"+arg+"</h5></td><td><h6>"+node.firstChild.nodeValue+"</h5></td><tr>";
            try:
                htmlNode = '<tr><td width=100 style="border-top: 1px solid #C0C0C0;">'+arg+'</td><td style="border-top: 1px solid #C0C0C0;">'+node.firstChild.nodeValue+'</td></tr>'
            except AttributeError:
                htmlNode = '<tr><td width=100 style="border-top: 1px solid #C0C0C0;">'+arg+'</td><td style="border-top: 1px solid #C0C0C0;">'+"N/A"+'</td></tr>'
            

        '''
        case "EXAMPLE":
                $exNo++;
                
                html = "<div class='panel-group' id='accordion'>
                          <div class='panel panel-info'>
                            <div class='panel-heading'>
                              <h4 class='panel-title'>
                                <a data-toggle='collapse' data-parent='#accordion' href='#collapse".$exNo."'>
                                  Example ".$exNo."
                                </a>
                              </h4>
                            </div>
                            <div id='collapse".$exNo."'  class='panel-collapse collapse in'>
                              <div class='panel-body'>
                                <div class='table'>";
        '''
                                
        for child in node.childNodes:
            # print(node.nodeName, child.nodeType)
            htmlNode += processXMLVerbNode(child)

        if node.nodeName.lower() == "roleset":
            None
            
        if node.nodeName.lower() == "roles":
            htmlNode += "</table>&nbsp;"

        if node.nodeName.lower() == "rel":
            htmlNode += "</td></tr>";

        if node.nodeName.lower() == "arg":
            htmlNode += "</td></tr>";

        if node.nodeName.lower() == "example":
            # htmlNode += '</table></div>' 
            # htmlNode += '</div>' 
            htmlNode += '</table></div></div>&nbsp;' 

    return htmlNode
      
class MyWebService(object):

    _myTabularView = None
    
    @cherrypy.expose
    def index(self):
        return open(BASE_HTML_PATH+'/index.php')

    def html(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def info(self, **params):
        return {"status":"online"}

    @cherrypy.expose
    def halt(self, **params):
            cherrypy.engine.exit()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def verbSenseFrame(self, predicate=None, senseNumber=None):
        global exampleNumber
        exampleNumber = 0
        input = { "text" : None , "anns" : [] }
        try:
            data = cherrypy.request.json
        except:
            data = cherrypy.request.params
        if "predicate" in data: input["predicate"] = data["predicate"]
        if "senseNumber" in data: input["senseNumber"] = data["senseNumber"]
        predicate = input["predicate"]
        senseNumber = input["senseNumber"]
        html = ""
        # html = "<h1>"+str(input["predicate"])+":"+str(input["senseNumber"])+"</h1>"
        html = "<h1>"+str(input["predicate"])+"</h1>"
        xmlFileName = "./frames/SRL-Verb/"+predicate.lower()+".xml"
        xmlFile = None
        try:
            xmlFile = open(xmlFileName,'r')
        except:
            None
        if xmlFile is None:
            html += '<div class="w3-panel w3-pale-red w3-border"><p>Verb frame not found.</p></div>'
        else:
            xmldoc = minidom.parse(xmlFile)
            xmlFile.close()
            rootNode = xmldoc.documentElement
            print("rootNode",rootNode,rootNode.tagName)
            html += processXMLVerbNode(rootNode)
        result = {"html": html}
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def nomSenseFrame(self, predicate=None, senseNumber=None):
        global exampleNumber
        exampleNumber = 0
        input = { "text" : None , "anns" : [] }
        try:
            data = cherrypy.request.json
        except:
            data = cherrypy.request.params
        if "predicate" in data: input["predicate"] = data["predicate"]
        if "senseNumber" in data: input["senseNumber"] = data["senseNumber"]
        predicate = input["predicate"]
        senseNumber = input["senseNumber"]
        html = ""
        # html = "<h1>"+str(input["predicate"])+":"+str(input["senseNumber"])+"</h1>"
        html = "<h1>"+str(input["predicate"])+"</h1>"
        xmlFileName = "./frames/SRL-Nom/"+predicate.lower()+".xml"
        xmlFile = None
        try:
            xmlFile = open(xmlFileName,'r')
        except:
            None
        if xmlFile is None:
            html += '<div class="w3-panel w3-pale-red w3-border"><p>Nom frame not found.</p></div>'
        else:
            xmldoc = minidom.parse(xmlFile)
            xmlFile.close()
            rootNode = xmldoc.documentElement
            print("rootNode",rootNode,rootNode.tagName)
            html += processXMLVerbNode(rootNode)
        result = {"html": html}
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def view(self, text=None, anns=None):
        input = { "text" : None , "anns" : [] }
        try:
            data = cherrypy.request.json
        except:
            data = cherrypy.request.params
        if "text" in data: input["text"] = data["text"]
        if "anns" in data: input["anns"] = data["anns"]
        # print(">>>>>>>>>", data["text"])
        self._myTabularView = tabular.TabularView()
        html = doProcess(self._myTabularView, data["text"] , data["anns"])
        result = {"input": input, "html": html}
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def cache(self):
        result = cache_dic
        return result
        
        
        

if __name__ == '__main__':
    print ("")
    print ("Starting 'CogComp' rest service...")
    config = {'server.socket_host': sys.argv[1]}
    cherrypy.config.update(config)
    config = {
      'global' : {
        'server.socket_host' : sys.argv[1],
        'server.socket_port' : int(sys.argv[2]),
        'cors.expose.on': True
      }, 
      '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())

      },
      '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': BASE_HTML_PATH
      },
      '/html' : {
        'tools.staticdir.on'    : True,
        'tools.staticdir.dir'   : BASE_HTML_PATH,
        'tools.staticdir.index' : 'index.html',
        'tools.gzip.on'         : True
      },
    }
    cherrypy.config.update(config)
    cherrypy.quickstart(MyWebService(), '/', config)

    cache.write(cache_dic)
