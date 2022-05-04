// Generated by gencpp from file ugv_ros/Stop.msg
// DO NOT EDIT!


#ifndef UGV_ROS_MESSAGE_STOP_H
#define UGV_ROS_MESSAGE_STOP_H

#include <ros/service_traits.h>


#include <ugv_ros/StopRequest.h>
#include <ugv_ros/StopResponse.h>


namespace ugv_ros
{

struct Stop
{

typedef StopRequest Request;
typedef StopResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct Stop
} // namespace ugv_ros


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::ugv_ros::Stop > {
  static const char* value()
  {
    return "c22f2a1ed8654a0b365f1bb3f7ff2c0f";
  }

  static const char* value(const ::ugv_ros::Stop&) { return value(); }
};

template<>
struct DataType< ::ugv_ros::Stop > {
  static const char* value()
  {
    return "ugv_ros/Stop";
  }

  static const char* value(const ::ugv_ros::Stop&) { return value(); }
};


// service_traits::MD5Sum< ::ugv_ros::StopRequest> should match
// service_traits::MD5Sum< ::ugv_ros::Stop >
template<>
struct MD5Sum< ::ugv_ros::StopRequest>
{
  static const char* value()
  {
    return MD5Sum< ::ugv_ros::Stop >::value();
  }
  static const char* value(const ::ugv_ros::StopRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::ugv_ros::StopRequest> should match
// service_traits::DataType< ::ugv_ros::Stop >
template<>
struct DataType< ::ugv_ros::StopRequest>
{
  static const char* value()
  {
    return DataType< ::ugv_ros::Stop >::value();
  }
  static const char* value(const ::ugv_ros::StopRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::ugv_ros::StopResponse> should match
// service_traits::MD5Sum< ::ugv_ros::Stop >
template<>
struct MD5Sum< ::ugv_ros::StopResponse>
{
  static const char* value()
  {
    return MD5Sum< ::ugv_ros::Stop >::value();
  }
  static const char* value(const ::ugv_ros::StopResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::ugv_ros::StopResponse> should match
// service_traits::DataType< ::ugv_ros::Stop >
template<>
struct DataType< ::ugv_ros::StopResponse>
{
  static const char* value()
  {
    return DataType< ::ugv_ros::Stop >::value();
  }
  static const char* value(const ::ugv_ros::StopResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // UGV_ROS_MESSAGE_STOP_H