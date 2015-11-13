#pragma once 

#include "../unit.h"

namespace signum::rnd
{
	class Dust : public Unit
	{
	public:
		Dust(UnitRef frequency);

		UnitRef frequency = nullptr;

		virtual sample next();
	
	private:
		int steps_remaining;

	};
}
