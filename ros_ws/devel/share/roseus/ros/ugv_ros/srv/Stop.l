;; Auto-generated. Do not edit!


(when (boundp 'ugv_ros::Stop)
  (if (not (find-package "UGV_ROS"))
    (make-package "UGV_ROS"))
  (shadow 'Stop (find-package "UGV_ROS")))
(unless (find-package "UGV_ROS::STOP")
  (make-package "UGV_ROS::STOP"))
(unless (find-package "UGV_ROS::STOPREQUEST")
  (make-package "UGV_ROS::STOPREQUEST"))
(unless (find-package "UGV_ROS::STOPRESPONSE")
  (make-package "UGV_ROS::STOPRESPONSE"))

(in-package "ROS")





(defclass ugv_ros::StopRequest
  :super ros::object
  :slots ())

(defmethod ugv_ros::StopRequest
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(defclass ugv_ros::StopResponse
  :super ros::object
  :slots (_result ))

(defmethod ugv_ros::StopResponse
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

(defclass ugv_ros::Stop
  :super ros::object
  :slots ())

(setf (get ugv_ros::Stop :md5sum-) "c22f2a1ed8654a0b365f1bb3f7ff2c0f")
(setf (get ugv_ros::Stop :datatype-) "ugv_ros/Stop")
(setf (get ugv_ros::Stop :request) ugv_ros::StopRequest)
(setf (get ugv_ros::Stop :response) ugv_ros::StopResponse)

(defmethod ugv_ros::StopRequest
  (:response () (instance ugv_ros::StopResponse :init)))

(setf (get ugv_ros::StopRequest :md5sum-) "c22f2a1ed8654a0b365f1bb3f7ff2c0f")
(setf (get ugv_ros::StopRequest :datatype-) "ugv_ros/StopRequest")
(setf (get ugv_ros::StopRequest :definition-)
      "
---
string result

")

(setf (get ugv_ros::StopResponse :md5sum-) "c22f2a1ed8654a0b365f1bb3f7ff2c0f")
(setf (get ugv_ros::StopResponse :datatype-) "ugv_ros/StopResponse")
(setf (get ugv_ros::StopResponse :definition-)
      "
---
string result

")



(provide :ugv_ros/Stop "c22f2a1ed8654a0b365f1bb3f7ff2c0f")


