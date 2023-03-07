#
# Copyright 2019-20 General Electric Company
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from . import sparqlconnection

import os.path
from semtk3.semtkclient import SemTkClient

class QueryClient(SemTkClient):
    
    def __init__(self, serverURL, conn_obj):
        ''' serverURL string - e.g. http://machine:12050
        '''
        super(QueryClient, self).__init__(serverURL, "sparqlQueryService")
        self.conn = conn_obj
    
    #
    # Download owl to a file
    # Default to data[0] graph in the connection
    # Raises exception on error
    # No return
    def exec_download_owl_file(self, owl_file_path, model_or_data=sparqlconnection.SparqlConnection.MODEL, index=0):
        
        payload = {
            "serverAndPort": self.conn.get_server_and_port(model_or_data, index),
            "serverType":    self.conn.get_server_type(model_or_data, index),
            "graph":       self.conn.get_graph(model_or_data, index),
            "user":          self.conn.get_user_name(),
            "password":      self.conn.get_password()
        }

        first_line = self.post_to_file("downloadOwlFile", payload, owl_file_path)
        if not "<rdf:RDF" in first_line:
            raise Exception("No rdf was returned.  e.g.: " + first_line)
        
            
    #
    # Upload owl.
    # Default to model[0] graph in the connection
    #
    def exec_upload_owl(self, owl_file_path, model_or_data=sparqlconnection.SparqlConnection.MODEL, index=0):
        
        payload = {
            "serverAndPort": self.conn.get_server_and_port(model_or_data, index),
            "serverType":    self.conn.get_server_type(model_or_data, index),
            "dataset":       self.conn.get_graph(model_or_data, index),
            "user":          self.conn.get_user_name(),
            "password":      self.conn.get_password()
        }
        
        files = {
            "owlFile": (os.path.basename(owl_file_path), open(owl_file_path, 'rb'))
        }

        res = self.post_to_status("uploadOwl", payload, files)
        return res
    
    #
    # Upload turtle.
    # Default to model[0] graph in the connection
    #
    def exec_upload_turtle(self, turtle_file_path, model_or_data=sparqlconnection.SparqlConnection.MODEL, index=0):
        
        payload = {
            "serverAndPort": self.conn.get_server_and_port(model_or_data, index),
            "serverType":    self.conn.get_server_type(model_or_data, index),
            "graph":         self.conn.get_graph(model_or_data, index),
            "user":          self.conn.get_user_name(),
            "password":      self.conn.get_password()
        }
        
        files = {
            "ttlFile": (os.path.basename(turtle_file_path), open(turtle_file_path, 'rb'))
        }

        res = self.post_to_status("uploadTurtle", payload, files)
        return res
    
    #
    # Execute query
    #
    def exec_query(self, query, model_or_data=sparqlconnection.SparqlConnection.DATA, index=0):
        
        payload = {
            "serverAndPort": self.conn.get_server_and_port(model_or_data, index),
            "serverType":    self.conn.get_server_type(model_or_data, index),
            "graph":         self.conn.get_graph(model_or_data, index),
            "resultType":    "TABLE",
            "query":         query
        }
      
        res = self.post_to_table("query", payload)
        return res

    #
    # Get graph names
    #
    def exec_select_graph_names(self, skip_semtk_graphs, graph_names_only):

        payload = {
            "serverAndPort": self.conn.get_server_and_port(sparqlconnection.SparqlConnection.MODEL, 0),
            "serverType":    self.conn.get_server_type(sparqlconnection.SparqlConnection.MODEL, 0),
            "skipSemtkGraphs": skip_semtk_graphs,
            "graphNamesOnly": graph_names_only
        }

        res = self.post_to_table("selectGraphNames", payload)
        return res
    
