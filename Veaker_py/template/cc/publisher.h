/*! 
 * @file {{message_name}}Publisher.h
 * This header file contains the declaration of the publisher functions.
 */

#ifndef {{message_name.upper()}}PUBLISHER_H
#define {{message_name.upper()}}PUBLISHER_H

#ifndef __SYNTHESIS__
#include <fastrtps/fastrtps_fwd.h>
#include <fastrtps/publisher/PublisherListener.h>
#endif // __SYNTHESIS__

#include "hls_stream.h"

#include "{{message_name}}.h"
#ifndef __SYNTHESIS__
#include "{{message_name}}PubSubTypes.h"
#endif // __SYNTHESIS__

class {{message_name}}Publisher : hls::stream< uint64_t > {
#ifndef __SYNTHESIS__
public:
    {{message_name}}Publisher(uint32_t dst);
    virtual ~{{message_name}}Publisher(void);
private:
	eprosima::fastrtps::Participant *mp_participant;
	eprosima::fastrtps::Publisher   *mp_publisher;

	class PubListener : public eprosima::fastrtps::PublisherListener {
	public:
		PubListener() : n_matched(0),publishable(false){};
		~PubListener(){};
		void onPublicationMatched(eprosima::fastrtps::Publisher* pub,eprosima::fastrtps::rtps::MatchingInfo& info);
		int n_matched;
        uint32_t n_destination;
        bool publishable;
	} m_listener;
    {{message_name}}PubSubType myType;
#endif // __SYNTHESIS__
public:
    void publish({{message_name}} &msg);
};

#endif // {{message_name.upper()}}PUBLISHER_H
