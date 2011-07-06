var callableType = function callableType(constructor) {
    return function() {
        var callableInstance = function() {
            var args = [];
            for (var i=0; i<arguments.length;i++) {
                args[i] = arguments[i];
            }
            //args.unshift($(this));
            args.unshift(this);
            return callableInstance.__call__.apply(callableInstance, args);
        };
        constructor.apply(callableInstance, arguments);
        return callableInstance;
    };
};

var Delegation;
Delegation = callableType(function(obj, func, data) {
    this.obj = obj;
    this.func = func;
    this.data = data;
    this.__call__ = function() {
        var args = [];
        for (var i=0; i<arguments.length; i++) {
            args[i] = arguments[i];
        }
        args.unshift(this.data);
        //console.log("Delegation.__call__",this.func,arguments);
        this.func.apply(this.obj, args);
    };
    this.destroy = function() {
        this.obj = null;
        this.func = null;
        this.data = null;
        delete this.obj;
        delete this.func;
        delete this.data;
    };
});

var Delegate;
Delegate = {
    context : null,
    delegations : [],
    create : function(obj, func, data) {
        var delegation = new Delegation(obj, func, data);
        if (data == "debug") console.log("delegation",obj,func,data);
        this.delegations.push(delegation);
        return delegation;
    },
    destroy : function() {
        for (var i=0; i<this.delegations.length; i++) {
            this.delegations[i].destroy();
            this.delegations[i] = null;
        }
        this.delegations = null;
        delete this.delegations;
    }
};

var Dispatcher;
Dispatcher = function Dispatcher(){
    this.__init__.apply(this, arguments);
};
Dispatcher.prototype.__init__ = function(){
    this.listeners = {};
    this.once = {};
    this.unique = {};
};
Dispatcher.prototype.addEventListener = function(event,callback,weight){
    if (typeof(event) != "string") {
        return;
    }
    if (!this.listeners[event]) this.listeners[event] = [];
    var info = {"callback":callback};
    this.listeners[event].push(info);
    if (weight) {
        this.listeners[event].sort(function(a, b) { return a.weight-b.weight; });
    }
};
Dispatcher.prototype.removeEventListener = function(){
    throw NI;
};
Dispatcher.prototype.dispatchEvent = function(event){
    var stack = this.listeners[event.type];
    if (stack) {
        for (var i=0; i<stack.length; i++) {
            stack[i].callback.call(this, event.data);
        }
    }
};


var Event;
Event = function Event(type,data){
    this.type = type;
    this.data = data;
};
Event.prototype.toString = function(){
    return "Event '"+this.type+"'";
};

Event.AJAX_PROGRESS = "ajaxProgress";
Event.AJAX_RESPONSE = "ajaxResponse";
Event.AJAX_SUCCESS = "ajaxSuccess";
Event.AJAX_NOT_FOUND = "ajaxNotFound";
Event.AJAX_SERVER_ERROR = "ajaxServerError";

Event.DATA_SEND = "dataSend";
Event.DATA_RECEIVE = "dataReceive";

