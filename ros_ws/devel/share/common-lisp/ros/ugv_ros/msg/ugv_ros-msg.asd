
(cl:in-package :asdf)

(defsystem "ugv_ros-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "xyyaw_pose" :depends-on ("_package_xyyaw_pose"))
    (:file "_package_xyyaw_pose" :depends-on ("_package"))
  ))