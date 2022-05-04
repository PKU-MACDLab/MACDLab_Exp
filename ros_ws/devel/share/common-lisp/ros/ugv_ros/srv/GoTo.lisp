; Auto-generated. Do not edit!


(cl:in-package ugv_ros-srv)


;//! \htmlinclude GoTo-request.msg.html

(cl:defclass <GoTo-request> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0)
   (yaw
    :reader yaw
    :initarg :yaw
    :type cl:float
    :initform 0.0))
)

(cl:defclass GoTo-request (<GoTo-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GoTo-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GoTo-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ugv_ros-srv:<GoTo-request> is deprecated: use ugv_ros-srv:GoTo-request instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <GoTo-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ugv_ros-srv:x-val is deprecated.  Use ugv_ros-srv:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <GoTo-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ugv_ros-srv:y-val is deprecated.  Use ugv_ros-srv:y instead.")
  (y m))

(cl:ensure-generic-function 'yaw-val :lambda-list '(m))
(cl:defmethod yaw-val ((m <GoTo-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ugv_ros-srv:yaw-val is deprecated.  Use ugv_ros-srv:yaw instead.")
  (yaw m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GoTo-request>) ostream)
  "Serializes a message object of type '<GoTo-request>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'yaw))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GoTo-request>) istream)
  "Deserializes a message object of type '<GoTo-request>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'yaw) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GoTo-request>)))
  "Returns string type for a service object of type '<GoTo-request>"
  "ugv_ros/GoToRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GoTo-request)))
  "Returns string type for a service object of type 'GoTo-request"
  "ugv_ros/GoToRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GoTo-request>)))
  "Returns md5sum for a message object of type '<GoTo-request>"
  "6535ac972b19122cf7fc9c3a775320c8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GoTo-request)))
  "Returns md5sum for a message object of type 'GoTo-request"
  "6535ac972b19122cf7fc9c3a775320c8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GoTo-request>)))
  "Returns full string definition for message of type '<GoTo-request>"
  (cl:format cl:nil "float64 x~%float64 y~%float64 yaw~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GoTo-request)))
  "Returns full string definition for message of type 'GoTo-request"
  (cl:format cl:nil "float64 x~%float64 y~%float64 yaw~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GoTo-request>))
  (cl:+ 0
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GoTo-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GoTo-request
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':yaw (yaw msg))
))
;//! \htmlinclude GoTo-response.msg.html

(cl:defclass <GoTo-response> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type cl:string
    :initform ""))
)

(cl:defclass GoTo-response (<GoTo-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GoTo-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GoTo-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ugv_ros-srv:<GoTo-response> is deprecated: use ugv_ros-srv:GoTo-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <GoTo-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ugv_ros-srv:result-val is deprecated.  Use ugv_ros-srv:result instead.")
  (result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GoTo-response>) ostream)
  "Serializes a message object of type '<GoTo-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'result))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'result))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GoTo-response>) istream)
  "Deserializes a message object of type '<GoTo-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'result) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'result) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GoTo-response>)))
  "Returns string type for a service object of type '<GoTo-response>"
  "ugv_ros/GoToResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GoTo-response)))
  "Returns string type for a service object of type 'GoTo-response"
  "ugv_ros/GoToResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GoTo-response>)))
  "Returns md5sum for a message object of type '<GoTo-response>"
  "6535ac972b19122cf7fc9c3a775320c8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GoTo-response)))
  "Returns md5sum for a message object of type 'GoTo-response"
  "6535ac972b19122cf7fc9c3a775320c8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GoTo-response>)))
  "Returns full string definition for message of type '<GoTo-response>"
  (cl:format cl:nil "string result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GoTo-response)))
  "Returns full string definition for message of type 'GoTo-response"
  (cl:format cl:nil "string result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GoTo-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'result))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GoTo-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GoTo-response
    (cl:cons ':result (result msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GoTo)))
  'GoTo-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GoTo)))
  'GoTo-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GoTo)))
  "Returns string type for a service object of type '<GoTo>"
  "ugv_ros/GoTo")