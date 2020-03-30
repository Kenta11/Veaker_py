/*! 
 * @file {{message_name}}Subscriber.h
 * This header file contains the declaration of the subscriber functions.
 */

#ifndef {{message_name.upper()}}_SUBSCRIBER_H
#define {{message_name.upper()}}_SUBSCRIBER_H

#ifndef __SYNTHESIS__
#include <mutex>
#include <queue>

#include <fastrtps/fastrtps_fwd.h>
#include <fastrtps/subscriber/SubscriberListener.h>
#include <fastrtps/subscriber/SampleInfo.h>
#endif // __SYNTHESIS__

#include "hls_stream.h"

#include "{{message_name}}.h"
#ifndef __SYNTHESIS__
#include "{{message_name}}PubSubTypes.h"
#endif // __SYNTHESIS__

class {{message_name}}Subscriber : hls::stream< uint64_t > {
#ifndef __SYNTHESIS__
public:
    {{message_name}}Subscriber(void);
    virtual ~{{message_name}}Subscriber(void);
private:
    eprosima::fastrtps::Participant *mp_participant;
	eprosima::fastrtps::Subscriber *mp_subscriber;

	class SubListener : public eprosima::fastrtps::SubscriberListener {
	public:
		SubListener() : n_matched(0),n_msg(0){};
		~SubListener(){};
		void onSubscriptionMatched(eprosima::fastrtps::Subscriber* sub,eprosima::fastrtps::rtps::MatchingInfo& info);
		void onNewDataMessage(eprosima::fastrtps::Subscriber* sub);
		eprosima::fastrtps::SampleInfo_t m_info;
		int n_matched;
		int n_msg;
        std::queue<{{message_name}}> buffer;
        std::mutex mtx;
	} m_listener;
    {{message_name}}PubSubType myType;
#endif // __SYNTHESIS__
public:
    {{message_name}} subscribe(void);
};

#endif // {{message_name.upper()}}_SUBSCRIBER_H
