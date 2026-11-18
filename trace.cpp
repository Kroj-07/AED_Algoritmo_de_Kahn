#include "kahn_interface.hpp"

TraceWriter::TraceWriter(const std::string& outPath): out_(outPath){
      if(!out_.is_open()){ std::cerr << "[TraceWriter] No se pudo abrir " << outPath << "\n"; }
    }

std::string TraceWriter::vecToJson(const std::vector<int>& v){
    std::string s = "[";
    for (size_t i = 0; i < v.size(); ++i) {
      if (i) s += ",";
        s += std::to_string(v[i]);
    } s += "]";
    return s;
  }

void TraceWriter::setGraph(int n, const std::vector<std::pair<int,int>>& edges){
      out_ << "{\n  \"n\": " << n << ",\n  \"edges\": [";
      for (size_t i = 0; i < edges.size(); ++i) {
        if (i) out_ << ",";
          out_ << "[" << edges[i].first << "," << edges[i].second << "]";
      } out_ << "],\n  \"events\": ["; // graphSet_ = true;
    }

void TraceWriter::writeEventHeader(const std::string& type){
    if (!firstEvent_) out_ << ",";
      firstEvent_ = false; out_ << "\n    {\"type\":\"" << type << "\"";
  }

void TraceWriter::init(const std::vector<int>& indegree, const std::vector<int>& queue){
        writeEventHeader("init");
      out_ << ", \"indegree\":" << vecToJson(indegree) << ", \"queue\":" << vecToJson(queue) << "}";
    }

void TraceWriter::pop(int node, const std::vector<int>& queue){
        writeEventHeader("pop");
      out_ << ", \"node\":" << node << ", \"queue\":" << vecToJson(queue) << "}";
    }

void TraceWriter::output(int node, const std::vector<int>& order){
        writeEventHeader("output");
      out_ << ", \"node\":" << node << ", \"order\":" << vecToJson(order) << "}";
    }

void TraceWriter::decrement(int from, int to, int newIndegree){
        writeEventHeader("decrement");
      out_ << ", \"from\":" << from << ", \"to\":" << to << ", \"indegree\":" << newIndegree << "}";
    }

void TraceWriter::push(int node, const std::vector<int>& queue){
        writeEventHeader("push");
      out_ << ", \"node\":" << node << ", \"queue\":" << vecToJson(queue) << "}";
    }

void TraceWriter::cycle(const std::vector<int>& remaining){
        writeEventHeader("cycle");
      out_ << ", \"remaining\":" << vecToJson(remaining) << "}";
    }

void TraceWriter::finish(const std::vector<int>& order, bool hasCycle){
        writeEventHeader("finish");
      out_ << ", \"order\":" << vecToJson(order) << ", \"hasCycle\":" << (hasCycle ? "true" : "false") << "}";
        //finished_ = true;
    }

void TraceWriter::flush(){
      out_ << "\n  ]\n}\n"; out_.flush();
    }