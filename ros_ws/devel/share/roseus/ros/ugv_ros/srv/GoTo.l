;; Auto-generated. Do not edit!


(when (boundp 'ugv_ros::GoTo)
  (if (not (find-package "UGV_ROS"))
    (make-package "UGV_ROS"))
  (shadow 'GoTo (find-package "UGV_ROS")))
(unless (find-package "UGV_ROS::GOTO")
  (make-package "UGV_ROS::GOTO"))
(unless (find-package "UGV_ROS::GOTOREQUEST")
  (make-package "UGV_ROS::GOTOREQUEST"))
(unless (find-package "UGV_ROS::GOTORESPONSE")
  (make-package "UGV_ROS::GOTORESPONSE"))

(in-package "ROS")





(defclass ugv_ros::GoToRequest
  :super ros::object
  :slots (_x _y _yaw ))

(defmethod ugv_ros::GoToRequest
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:yaw __yaw) 0.0)
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _yaw (float __yaw))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:yaw
   (&optional __yaw)
   (if __yaw (setq _yaw __yaw)) _yaw)
  (:serialization-length
   ()
   (+
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _yaw
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _yaw
       (sys::poke _yaw (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _yaw
     (setq _yaw (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass ugv_ros::GoToResponse
  :super ros::object
  :slots (_result ))

(defmethod ugv_ros::GoToResponse
  (:init
   (&key
    ((:result __result) "")
    )
   (send-super :init)
   (setq _result (string __result))
   self)
  (:result
   (&optional __result)
   (if __result (setq _result __result)) _result)
  (:serialization-length
   ()
   (+
    ;; string _result
    4 (length _result)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _result
       (write-long (length _result) s) (princ _result s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _result
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _result (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass ugv_ros::GoTo
  :super ros::object
  :slots ())

(setf (get ugv_ros::GoTo :md5sum-) "6535ac972b19122cf7fc9c3a775320c8")
(setf (get ugv_ros::GoTo :datatype-) "ugv_ros/GoTo")
(setf (get ugv_ros::GoTo :request) ugv_ros::GoToRequest)
(setf (get ugv_ros::GoTo :response) ugv_ros::GoToResponse)

(defmethod ugv_ros::GoToRequest
  (:response () (instance ugv_ros::GoToResponse :init)))

(setf (get ugv_ros::GoToRequest :md5sum-) "6535ac972b19122cf7fc9c3a775320c8")
(setf (get ugv_ros::GoToRequest :datatype-) "ugv_ros/GoToRequest")
(setf (get ugv_ros::GoToRequest :definition-)
      "float64 x
float64 y
float64 yaw
---
string result

")

(setf (get ugv_ros::GoToResponse :md5sum-) "6535ac972b19122cf7fc9c3a775320c8")
(setf (get ugv_ros::GoToResponse :datatype-) "ugv_ros/GoToResponse")
(setf (get ugv_ros::GoToResponse :definition-)
      "float64 x
float64 y
float64 yaw
---
string result

")



(provide :ugv_ros/GoTo "6535ac972b19122cf7fc9c3a775320c8")


